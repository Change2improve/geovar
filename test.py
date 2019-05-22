from onshapepy import *
import requests

did = "04b732c124cfa152cf7c07f3"
wid = "c4358308cbf0c97a44d8a71a"
eid = "a23208c314d70c14da7071e6"


part_URL    = "https://cad.onshape.com/documents/{}/w/{}/e/{}".format(did,wid,eid)
myPart = Part( part_URL )
c      = Client()



res = c._api.request('get', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/configuration')

payload = {
    "configurationParameters" : [ {
        "type" : 1826,
        "typeName" : "BTMConfigurationParameterQuantity",
        "message" : {
          "quantityType" : "LENGTH",
          "rangeAndDefault" : {
            "type" : 181,
            "typeName" : "BTQuantityRange",
            "message" : {
              "units" : "millimeter",
              "minValue" : 10.0,
              "maxValue" : 100.0,
              "defaultValue" : 25.0,
              "location" : {
                "type" : 226,
                "typeName" : "BTLocationInfo",
                "message" : {
                  "document" : "",
                  "version" : "",
                  "topLevel" : "",
                  "parseNodeId" : "",
                  "character" : 0,
                  "line" : 0,
                  "column" : 0,
                  "endCharacter" : 0,
                  "endLine" : 0,
                  "endColumn" : 0,
                  "languageVersion" : 0,
                  "moduleIds" : {
                    "type" : 1897,
                    "typeName" : "BTDocumentVersionElementIds",
                    "message" : {
                      "documentId" : "",
                      "versionId" : "",
                      "elementId" : ""
                    }
                  },
                  "elementMicroversion" : "",
                  "nodeId" : "nFreFwoXwUZQobSH"
                }
              }
            }
          },
          "parameterId" : "r_inner",
          "parameterName" : "r_inner",
          "hasUserCode" : False,
          "nodeId" : "MMR4m/NPKrN4Sd1hj"
        }
      }, {
        "type" : 1826,
        "typeName" : "BTMConfigurationParameterQuantity",
        "message" : {
          "quantityType" : "LENGTH",
          "rangeAndDefault" : {
            "type" : 181,
            "typeName" : "BTQuantityRange",
            "message" : {
              "units" : "millimeter",
              "minValue" : 10.0,
              "maxValue" : 150.0,
              "defaultValue" : 100.0,
              "location" : {
                "type" : 226,
                "typeName" : "BTLocationInfo",
                "message" : {
                  "document" : "",
                  "version" : "",
                  "topLevel" : "",
                  "parseNodeId" : "",
                  "character" : 0,
                  "line" : 0,
                  "column" : 0,
                  "endCharacter" : 0,
                  "endLine" : 0,
                  "endColumn" : 0,
                  "languageVersion" : 0,
                  "moduleIds" : {
                    "type" : 1897,
                    "typeName" : "BTDocumentVersionElementIds",
                    "message" : {
                      "documentId" : "",
                      "versionId" : "",
                      "elementId" : ""
                    }
                  },
                  "elementMicroversion" : "",
                  "nodeId" : "gGoV+btibJ0cVuxZ"
                }
              }
            }
          },
          "parameterId" : "r_outer",
          "parameterName" : "r_outer",
          "hasUserCode" : False,
          "nodeId" : "MnLzlzxZhiJmepzxe"
        }
      }, {
        "type" : 1826,
        "typeName" : "BTMConfigurationParameterQuantity",
        "message" : {
          "quantityType" : "LENGTH",
          "rangeAndDefault" : {
            "type" : 181,
            "typeName" : "BTQuantityRange",
            "message" : {
              "units" : "millimeter",
              "minValue" : 10.0,
              "maxValue" : 200.0,
              "defaultValue" : 100.0,
              "location" : {
                "type" : 226,
                "typeName" : "BTLocationInfo",
                "message" : {
                  "document" : "",
                  "version" : "",
                  "topLevel" : "",
                  "parseNodeId" : "",
                  "character" : 0,
                  "line" : 0,
                  "column" : 0,
                  "endCharacter" : 0,
                  "endLine" : 0,
                  "endColumn" : 0,
                  "languageVersion" : 0,
                  "moduleIds" : {
                    "type" : 1897,
                    "typeName" : "BTDocumentVersionElementIds",
                    "message" : {
                      "documentId" : "",
                      "versionId" : "",
                      "elementId" : ""
                    }
                  },
                  "elementMicroversion" : "",
                  "nodeId" : "35mt5XiKD/PGjYU5"
                }
              }
            }
          },
          "parameterId" : "height",
          "parameterName" : "height",
          "hasUserCode" : False,
          "nodeId" : "MRM+vgqf99B3mQ1Lu"
        }
      } ],
      "currentConfiguration" : [ {
        "type" : 147,
        "typeName" : "BTMParameterQuantity",
        "message" : {
          "units" : "millimeter",
          "value" : 65.0,
          "expression" : "65 mm",
          "isInteger" : False,
          "parameterId" : "r_inner",
          "hasUserCode" : False,
          "nodeId" : "M54CVS3ZuAx6OJ+/d"
        }
      }, {
        "type" : 147,
        "typeName" : "BTMParameterQuantity",
        "message" : {
          "units" : "millimeter",
          "value" : 100.0,
          "expression" : "100 mm",
          "isInteger" : False,
          "parameterId" : "r_outer",
          "hasUserCode" : False,
          "nodeId" : "Mjt6mKY2zttH4gwr0"
        }
      }, {
        "type" : 147,
        "typeName" : "BTMParameterQuantity",
        "message" : {
          "units" : "millimeter",
          "value" : 100.0,
          "expression" : "100 mm",
          "isInteger" : False,
          "parameterId" : "height",
          "hasUserCode" : False,
          "nodeId" : "MqK6pb4C6pdlH5QME"
        }
      } ],
      "serializationVersion" : "1.1.17",
      "sourceMicroversion" : "657289f18ed81a845ac81941",
      "rejectMicroversionSkew" : False,
      "microversionSkew" : True,
      "libraryVersion" : 1063
}

payload2 = {
   "currentConfiguration" : [ { "units" : "millimeter", "value" : 65.0, "expression" : "65 mm" } ]
} 

res = c._api.request('post', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/configuration', body=payload)
