import logging
from pprint import pprint

from cp_translator.src.translation.processor.mapper import init_mapper

logger = logging.getLogger(__name__)


class CPProcessor:

    def __init__(self, mapper):
        """
        constructor for MessageProcessor

        :param avro_serializer: shared specific avro_serializer
        :type avro_serializer: AvroSerializer
        :param avro_deserializer: shared specific avro_deserializer
        :type avro_deserializer: AvroDeserializer
        :param http_client: http client to download the blob
        :type http_client: HttpClient
        """
        self.mapper = mapper

    def map(self, data_dict):
        try:
            results = self.mapper.map(data_dict)
            return results
        except Exception as exc:
            raise exc


if __name__ == "__main__":
    mapper = init_mapper()
    cp_processor = CPProcessor(mapper)
    data = {
  "ProdKey": "MSC52226",
  "Description": "qui dolorem ipsum",
  "StoreCode": "DellStaples - HP 1KU36UA#ABA (DellStaples)",
  "Market": "West",
  "Comments": "Quis autem vel eum iure reprehenderit, qui in ea voluptate velit esse.",
  "CompetitorProdKey": "2ac2e7e7-a6e9-4d5b-b1fd-62b8036b89e6",
  "expected_result": "SUCCESS",
  "EffectiveDate": "2018-10-25 09:20:40.602156",
  "Price": "44.9900",
  "Quantity": 2,
  "PriceType": "Normalpris"
}
    results = cp_processor.map(data)
    print("Results are")
    pprint(results)


