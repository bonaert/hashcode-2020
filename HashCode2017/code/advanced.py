import operator
import random

from data import Data
#
#
# def solve:
#     videos_in_caches
#     for cache in caches:
#         videos_in_cache = []
#         space = default_space
#         videos_in_order_of_time_saved = get_videos_in_order_of_time_saved(cache)
#         for video in videos_in_order_of_time_saved:
#             video -> videos_in_cache
#             update
#             best_latency
#             for the video for the differrent endpoints
#
#             if video_size > space:
#                 break
#         videos_in_cache -> videos_in_caches
#
#     output(videos_in_caches)


def get_caches_in_good_order(data):
    # TODO: I process cache 0 -> n, but there could be a better order
    # Example: the most connected cache, or the cache that most improves latency
    # or things like that

    # Bizarelly, this has a worse score than simply return range(data.num_caches) :(
    # TODO: I could try an average times_saved, instead of an absolute (because that one is going to
    # prioritize the caches that are connected to most endpoints)
    # Tried it. It's also worse. I don't really understand why
    
    # For now, the best ordering is, bizarelly, this:
    return range(data.num_caches)
    
    cache_scores = {}
    for cache in data.cache_to_endpoint_latencies:
    	sum_saved_latency = 0
    	num_saved_latency = len(data.cache_to_endpoint_latencies[cache])
        
        for (endpoint, latency) in data.cache_to_endpoint_latencies[cache].items():
            saved_latency = max(data.endpoint_to_datacenter_latencies[endpoint] - latency,0)
            num_saved_latency += saved_latency


            #cache_scores[cache] += saved_latency * data.num_requests_for_endpoint[endpoint]
        cache_scores[cache] = sum_saved_latency/num_saved_latency

    data = sorted(cache_scores.items(), key=operator.itemgetter(1), reverse=True)
    return [cache for (cache, score) in data]
    # return range(data.num_caches)


def solve_problem(filename):
    print("Parsing file for %s" % filename)
    data = Data("../Data/%s.in" % filename)

    print("Processing file %s" % filename)
    videos_in_caches = []

    ordered_caches = get_caches_in_good_order(data)
    print(ordered_caches)

    num_caches_treated = 0
    for cache in ordered_caches:
    	print(cache, " Num ", num_caches_treated)
    	num_caches_treated += 1
        videos_in_cache = []
        remaining_space = data.cache_size

        for (video, time_saved) in get_videos_in_order_of_time_saved(cache, data):
            if data.video_sizes[video] > remaining_space:
                continue

            if remaining_space <= 0:
                break

            videos_in_cache.append(video)
            remaining_space -= data.video_sizes[video]
            update_best_latency_info(data, video, cache)


        videos_in_caches.append(videos_in_cache)

    print("Writing result for file %s" % filename)
    write_to_file(filename, data, videos_in_caches)


def update_best_latency_info(data, video, cache):
    """
    Update the data.best_latency[video][endpoint] dict
    """
    best_latency_for_video = data.best_latency[video]
    for (endpoint, latency) in best_latency_for_video.items():
        # If the cache is connected to the endpoint
        if endpoint in data.cache_to_endpoint_latencies[cache]:
            new_latency = data.cache_to_endpoint_latencies[cache][endpoint]

            if new_latency < latency:
                best_latency_for_video[endpoint] = new_latency


def write_to_file(filename, data, videos_in_caches):
    with open("%s.greg" % filename, 'w') as f:
        f.write(str(data.num_caches))
        f.write('\n')

        for (num_cache, videos_in_cache) in enumerate(videos_in_caches):
            # print(videos_in_cache)
            f.write("%d " % num_cache)
            f.write(' '.join(map(str, videos_in_cache)))
            f.write('\n')


def get_videos_in_order_of_time_saved(cache, data):#: Data):
    """ Returns (video, time_saved) list """
    time_saved_per_video = get_time_saved_dict(cache, data)
    return sorted(time_saved_per_video.items(), key=operator.itemgetter(1), reverse=True)



def get_time_saved_dict(cache, data):#: Data):
    """ Returns a {video: time_saved} dict
    self.endpoint_to_videos[endpoint]
    self.best_latency[video][endpoint]
    """
    score = {}
    for (video, endpoint, req) in data.get_videos_and_endpoints_linked_to_cache(cache):
        best_latency = data.best_latency[video][endpoint]
        current_latency = data.cache_to_endpoint_latencies[cache][endpoint]
        saved_latency = max(best_latency - current_latency, 0)

        if video not in score:
            score[video] = 0

        # Best scoring function seems to be:
        score[video] += req * saved_latency / data.video_sizes[video]
        
        # Test: makes it slightly worse
        # score[video] += req * saved_latency / (data.video_sizes[video] ** 0.5)
        # First attempt
        # score[video] += req * saved_latency
    return score


solve_problem("me_at_the_zoo")
solve_problem("videos_worth_spreading")
solve_problem("trending_today")
solve_problem("kittens")