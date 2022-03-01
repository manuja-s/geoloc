from rest_framework.views import APIView
from rest_framework.response import Response
import dicttoxml
import requests
import json


class Geolocation(APIView):

    def put(self, request):
        requested_address = request.data
        url = "https://maps.googleapis.com/maps/api/geocode/json?address="
        address = requested_address["address"]
        output_format = requested_address["output_format"]
        key = "&key="  # Insert API-key here
        geo_location = url + address.replace(' ', '+').replace('#', '') + key
        data = requests.get(geo_location)  # requesting url through browser
        geoloc = json.loads(data.text)     # extracting the response
        location = {
            "coordinates": geoloc["results"][0]["geometry"]["location"],
            "address": geoloc["results"][0]["formatted_address"]
        }
        if output_format == "xml":
            xml = dicttoxml.dicttoxml(location, attr_type=False)  # XML format will display
            return Response(xml)
        elif output_format == "json":
            return Response(location)   # JSON format will display
        else:
            return Response({"error": "Enter the format XML o JSON"})
