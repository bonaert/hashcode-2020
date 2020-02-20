import copy


def line_to_ints(line):
    data = line.strip().split()
    return [int(x) for x in data]


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
        self.endpoint_to_cache_latencies
        self.endpoint_to_datacenter_latency
        self.cache_to_endpoint_latencies
        self.cache_to_endpoint_saved_time
        self.cache_to_videos: {cache: [video1, video2, ...], cache2: [video1, video3, ...] }
        self.video_endpoint_best_time {video: {cache: best_time, ...}, video2: ...
        """

        self.parse_file(filename)


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
            self.cache_to_endpoint_saved_latencies = {}
            self.best_ready_latency = {}
            self.num_connected_caches_haha = {}
            self.video_endpoint_best_time = {}
            for num_endpoint in range(self.num_endpoints):
                datacenter_latency, num_connected_caches = line_to_ints(f.readline())
                self.num_connected_caches_haha[num_endpoint] = num_connected_caches
                cache_latencies = {}
                self.endpoint_to_datacenter_latencies[num_endpoint] = datacenter_latency
                self.best_ready_latency[num_endpoint] = datacenter_latency
                for j in range(num_connected_caches):
                    cache_num, latency = line_to_ints(f.readline())
                    cache_latencies[cache_num] = latency

                    info = {"latency": latency, "endpoint": num_endpoint}
                    if cache_num in self.cache_to_endpoint_latencies:
                        self.cache_to_endpoint_latencies[cache_num].append(info)
                    else:
                        self.cache_to_endpoint_latencies[cache_num] = [info]

                    info = {"saved_latency": self.best_ready_latency[num_endpoint] - latency, "endpoint": num_endpoint}
                    if cache_num in self.cache_to_endpoint_saved_latencies:
                        self.cache_to_endpoint_saved_latencies[cache_num].append(info)
                    else:
                        self.cache_to_endpoint_saved_latencies[cache_num] = [info]

                self.endpoint_to_cache_latencies[num_endpoint] = cache_latencies

            self.request_descriptions = []
            self.requests_for_endpoint = {}
            for num_endpoint in range(self.num_request_desc):
                video_num, endpoint, num_requests = line_to_ints(f.readline())
                request_desc_dict = {"video_num": video_num,
                                     "endpoint": endpoint,
                                     "num_requests": num_requests}
                self.request_descriptions.append(request_desc_dict)

                info = {"video_num": video_num, "num_requests": num_requests}
                if endpoint in self.requests_for_endpoint:
                    self.requests_for_endpoint[endpoint].append(info)
                else:
                    self.requests_for_endpoint[endpoint] = [info]


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
