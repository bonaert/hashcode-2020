from code.hashcode import Data
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

    data = Data("../Data/me_at_the_zoo.in")

    data_center_dic = {}

    for cache in data.cache_to_endpoint_latencies:
        data_center_dic[cache] = ["x"]

    print(data_center_dic)

    for endpoint in data.requests_for_endpoint:

        nb_request=0
        for elem in data.requests_for_endpoint[endpoint]:
            nb_request += elem["num_requests"]

        print("ENDPOINT" + str(endpoint))
        latence_to_data_center = data.endpoint_to_datacenter_latencies[endpoint]

        best_lat = latence_to_data_center
        fournisseur_with_best_lat = "DATACENTER"

        for cache in data.endpoint_to_cache_latencies[endpoint]:
            value = data.endpoint_to_cache_latencies[endpoint][cache]
            print(value)

            if value < best_lat:
                best_lat = value
                fournisseur_with_best_lat = cache

        print("BEST_LAT " + str(best_lat) + " from " + str(fournisseur_with_best_lat))


        tmp_eco = nb_request * (latence_to_data_center - best_lat)

        if  data_center_dic[fournisseur_with_best_lat] != "x" and tmp_eco < data_center_dic[fournisseur_with_best_lat]:
            data_center_dic[fournisseur_with_best_lat] = endpoint

        elif data_center_dic[fournisseur_with_best_lat] == "x":
            data_center_dic[fournisseur_with_best_lat] = endpoint



print(data_center_dic)

for cache in data_center_dic:

    my_vids = []


    endpoint = data_center_dic[cache]

    if endpoint != 'x':

        for video in data.requests_for_endpoint[endpoint]:
            video_num = video["video_num"]

            if len(my_vids) <  data.metadata["cache_size"]:
                my_vids.append(video_num)


    print( "CACHE " + str(cache) + str(my_vids))
























