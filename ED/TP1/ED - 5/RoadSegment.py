class RoadSegment:


    def __init__(self, gid, osm_id, oneway, bridge, tunnel, type):
        self.gid = gid
        self.osm_id = osm_id
        self.oneway = oneway
        self.bridge = bridge
        self.tunnel = tunnel
        self.type = type