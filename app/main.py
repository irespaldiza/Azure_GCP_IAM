import os
import sys

import msal
import requests


def required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Falta la variable {name}")
    return value


def request_json(method: str, url: str, **kwargs) -> dict:
    response = requests.request(method, url, timeout=30, **kwargs)
    if not response.ok:
        raise RuntimeError(
            f"{method} {url} fallo con HTTP {response.status_code}: {response.text}"
        )
    return response.json()


def main() -> None:
    tenant_id = required("AZURE_TENANT_ID")
    client_id = required("AZURE_CLIENT_ID")
    client_secret = required("AZURE_CLIENT_SECRET")
    project_id = required("GCP_PROJECT_ID")
    project_number = required("GCP_PROJECT_NUMBER")
    pool_id = required("GCP_WORKLOAD_POOL_ID")
    provider_id = required("GCP_WORKLOAD_PROVIDER_ID")
    service_account = required("GCP_SERVICE_ACCOUNT_EMAIL")

    entra = msal.ConfidentialClientApplication(
        client_id=client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential=client_secret,
    )
    entra_result = entra.acquire_token_for_client(scopes=[f"api://{client_id}/.default"])
    entra_token = entra_result.get("access_token")
    if not entra_token:
        raise RuntimeError(f"Entra ID no emitio un token: {entra_result}")
    print("1. Token obtenido de Microsoft Entra ID")

    audience = (
        f"//iam.googleapis.com/projects/{project_number}/locations/global/"
        f"workloadIdentityPools/{pool_id}/providers/{provider_id}"
    )
    sts_result = request_json(
        "POST",
        "https://sts.googleapis.com/v1/token",
        data={
            "audience": audience,
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "requested_token_type": "urn:ietf:params:oauth:token-type:access_token",
            "scope": "https://www.googleapis.com/auth/cloud-platform",
            "subject_token": entra_token,
            "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
        },
    )
    federated_token = sts_result["access_token"]
    print("2. Token federado obtenido de Google STS")

    impersonation_url = (
        "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/"
        f"{service_account}:generateAccessToken"
    )
    impersonation_result = request_json(
        "POST",
        impersonation_url,
        headers={"Authorization": f"Bearer {federated_token}"},
        json={
            "scope": ["https://www.googleapis.com/auth/cloud-platform"],
            "lifetime": "3600s",
        },
    )
    google_token = impersonation_result["accessToken"]
    print("3. Service account suplantada correctamente")

    project = request_json(
        "GET",
        f"https://cloudresourcemanager.googleapis.com/v3/projects/{project_id}",
        headers={"Authorization": f"Bearer {google_token}"},
    )
    print(f"4. Proyecto consultado: {project['projectId']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
