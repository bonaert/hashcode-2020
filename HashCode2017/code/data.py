import copy


def line_to_ints(line):
    data = line.strip().split()
    return [int(x) for x in data]


# noinspection PyAttributeOutsideInit
class Data:
    def __init__(self, filename):
        """
        Here's the fields available:
        self.num_videos
        self.num_endpoints
        self.num_request_desc
        self.num_caches
        self.cache_size
        self.metadata
        self.metadata
        self.video_sizes
        self.request_descriptions
        self.requests_for_endpoint

        self.endpoint_to_datacenter_latency
        self.cache_to_endpoint_latencies
        self.cache_to_endpoint_saved_time
        self.cache_to_videos: {cache: [video1, video2, ...], cache2: [video1, video3, ...] }
        self.video_endpoint_best_time {video: {cache: best_time, ...}, video2: ...

        Ce dont j'ai besoin:

        TODO:
        video_and_endpoints_connected_to_cache(cache):
        cache_to_endpoints:
        self.caches_to_info[cache][endpoint][video]

        DONE
        self.best_latency[video][endpoint]: au début ça vaut datacenter_legacy (pour ce endpoint)
        self.endpoint_to_cache_latencies
        """
        self.parse_file(filename)
        self.build_best_latency_dict()
        self.build_endpoint_to_videos_dict()

    def build_endpoint_to_videos_dict(self):
        """ Build self.endpoint_to_videos[endpoint] """
        self.endpoint_to_video_requests = {}
        for (endpoint, request_list_for_endpoint) in self.requests_for_endpoint.items():
            for request in request_list_for_endpoint:
                if endpoint not in self.endpoint_to_video_requests:
                    self.endpoint_to_video_requests[endpoint] = []

                video_num = request["video_num"]
                num_requests = request["num_requests"]
                self.endpoint_to_video_requests[endpoint].append((video_num, num_requests))

    def get_videos_and_endpoints_linked_to_cache(self, cache):
        """ Yield (endpoint, video, num_requests) pairs linked to cache """
        for endpoint in self.cache_to_endpoint_latencies[cache].keys():
            for (video, num_requests) in self.endpoint_to_video_requests[endpoint]:
                yield (video, endpoint, num_requests)

    def build_best_latency_dict(self):
        self.best_latency = {}
        # print(self.requests_for_endpoint)
        for (endpoint, requests) in self.requests_for_endpoint.items():
            # print()
            # print(endpoint, requests)
            for request in requests:
                video_num = request['video_num']

                if video_num not in self.best_latency:
                    self.best_latency[video_num] = {}

                latency = self.endpoint_to_datacenter_latencies[endpoint]
                self.best_latency[video_num][endpoint] = latency
            # print(self.best_latency)

    def parse_file(self, filename):
        with open(filename, 'r') as f:
            metadata = line_to_ints(f.readline())
            self.num_videos, self.num_endpoints, self.num_request_desc, self.num_caches, self.cache_size = metadata
            self.metadata = {
                "num_videos": self.num_videos,
                "num_endpoints": self.num_endpoints,
                "num_request_desc": self.num_request_desc,
                "num_caches": self.num_caches,
                "cache_size": self.cache_size
            }

            self.video_sizes = line_to_ints(f.readline())

            self.endpoint_to_datacenter_latencies = {}
            self.endpoint_to_cache_latencies = {}
            self.cache_to_endpoint_latencies = {}
            self.num_connected_caches_haha = {}
            self.num_requests_for_endpoint = {}
            for num_endpoint in range(self.num_endpoints):
                datacenter_latency, num_connected_caches = line_to_ints(f.readline())
                self.num_connected_caches_haha[num_endpoint] = num_connected_caches
                cache_latencies = {}
                self.endpoint_to_datacenter_latencies[num_endpoint] = datacenter_latency
                for j in range(num_connected_caches):
                    cache_num, latency = line_to_ints(f.readline())
                    cache_latencies[cache_num] = latency

                    if cache_num not in self.cache_to_endpoint_latencies:
                        self.cache_to_endpoint_latencies[cache_num] = {}

                    self.cache_to_endpoint_latencies[cache_num][num_endpoint] = latency

                self.endpoint_to_cache_latencies[num_endpoint] = cache_latencies

            self.request_descriptions = []
            self.requests_for_endpoint = {}
            self.num_requests_for_endpoint = {}
            for num_endpoint in range(self.num_request_desc):
                video_num, endpoint, num_requests = line_to_ints(f.readline())
                request_desc_dict = {"video_num": video_num,
                                     "endpoint": endpoint,
                                     "num_requests": num_requests}
                self.request_descriptions.append(request_desc_dict)

                info = {"video_num": video_num, "num_requests": num_requests}
                if endpoint in self.requests_for_endpoint:
                    self.requests_for_endpoint[endpoint].append(info)
                    self.num_requests_for_endpoint[endpoint] += num_requests
                else:
                    self.requests_for_endpoint[endpoint] = [info]
                    self.num_requests_for_endpoint[endpoint] = num_requests


if __name__ == '__main__':
    data = Data("../Data/me_at_the_zoo.in")
    print("Metadata: %s" % data.metadata)
    print("Video sizes: %s" % data.video_sizes)
    print("Request descriptions: %s" % data.request_descriptions)
    print("Requests for endpoint: %s" % data.requests_for_endpoint)
    print("Endpoints to datacenter latencies: %s " % data.endpoint_to_datacenter_latencies)
    print("Endpoints to cache latencies: %s " % data.endpoint_to_cache_latencies)
    print("Cache to endpoint latencies: %s" % data.cache_to_endpoint_latencies)
    print("Cache to endpoint saved latencies: %s" % data.cache_to_endpoint_saved_latencies)
