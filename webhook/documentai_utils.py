# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
import os

from google.cloud import documentai
from google.api_core.client_options import ClientOptions

DOCAI_PROCESSOR = os.environ["DOCAI_PROCESSOR"]
DOCAI_LOCATION = os.environ["DOCAI_LOCATION"]


def get_document_text(project_id: str, gcs_uri: str, mime_type: str) -> str:
    """Perform Optical Character Recognition (OCR) with Document AI on Cloud Storage files.

    For more information, see:
        https://cloud.google.com/document-ai/docs/process-documents-ocr

    Args:
        input_file_gcs_uri: GCS URI of the PDF/TIFF file.
    """
    # You must set the `api_endpoint` if you use a location other than "us".
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{DOCAI_LOCATION}-documentai.googleapis.com"
        )
    )
    response = client.process_document(
        request=documentai.ProcessRequest(
            name=client.processor_path(project_id, "us", DOCAI_PROCESSOR),
            gcs_document=documentai.GcsDocument(
                gcs_uri=gcs_uri,
                mime_type=mime_type,
            ),
        ),
    )
    return response.document.text