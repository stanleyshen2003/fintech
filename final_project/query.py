from typing import List

from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine
from google.protobuf.json_format import MessageToDict

# TODO(developer): Uncomment these variables before running the sample.
project_id = "tw-rd-tam-stanleyshen"
location = "global"          # Values: "global", "us", "eu"
engine_id = "esun-insurance_1729776330935"
search_query = "匯款銀行及中間行所收取之相關費用由誰負擔?"


def client_create(
    project_id: str,
    location: str,
    engine_id: str,
) -> List[discoveryengine.SearchResponse]:
    
    client_options = (None)

    # Create a client
    client = discoveryengine.SearchServiceClient(client_options=client_options)

    # The full resource name of the search app serving config
    serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_config"

    content_search_spec = discoveryengine.SearchRequest.ContentSearchSpec(
        snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
            return_snippet=False
        )
    )
    
    return client, serving_config, content_search_spec

def query(client, serving_config, content_search_spec, search_query):

    # Refer to the `SearchRequest` reference for all supported fields:
    # https://cloud.google.com/python/docs/reference/discoveryengine/latest/google.cloud.discoveryengine_v1.types.SearchRequest
    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=search_query,
        page_size=50,
        content_search_spec=content_search_spec,
        query_expansion_spec=discoveryengine.SearchRequest.QueryExpansionSpec(
            condition=discoveryengine.SearchRequest.QueryExpansionSpec.Condition.AUTO,
        ),
        spell_correction_spec=discoveryengine.SearchRequest.SpellCorrectionSpec(
            mode=discoveryengine.SearchRequest.SpellCorrectionSpec.Mode.AUTO
        ),
    )

    response = client.search(request)
    result = [int(dict(doc.document.derived_struct_data)['title']) for doc in response.results]

    return result

client, serving_config, content_search_spec = client_create(project_id, location, engine_id)
result = query(client, serving_config, content_search_spec, search_query)
print(result)