import onshape_client

did = "04b732c124cfa152cf7c07f3"
wid = "c4358308cbf0c97a44d8a71a"
eid = "a23208c314d70c14da7071e6"


part_URL    = "https://cad.onshape.com/documents/{}/w/{}/e/{}".format(did,wid,eid)
myPart = Part( part_URL )
c      = Client()
res = c._api.request('get', '/api/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/configuration')

