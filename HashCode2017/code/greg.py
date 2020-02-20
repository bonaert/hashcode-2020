import operator

from code.hashcode import Data

def solve_problem(filename):
    print(filename)

    problem_data = Data("../Data/%s.in" % filename)


    videos_in_caches = []
    for cache in range(problem_data.num_caches):
        remaining_space = problem_data.cache_size

        # Trie les endpoints par latency sauvée
        saved = problem_data.cache_to_endpoint_saved_latencies[cache]
        data = [(d['saved_latency'], d['endpoint']) for d in saved]
        data = sorted(data)[::-1]

        videos = set()


        for (saved_latency, endpoint) in data:
            requests = problem_data.requests_for_endpoint[endpoint]
            # print(requests)

            request_timing = [(d['num_requests'], d['video_num']) for d in requests]

            # This is a list of (num_requests, video_num)
            request_timing = sorted(request_timing)[::-1]
            # print(request_timing)

            for (num_requests, video) in request_timing:
                videos.add(video)
                remaining_space -= problem_data.video_sizes[video]

                if remaining_space < 0:
                    videos.remove(video)
                    break

            if remaining_space <= 0:
                break

        videos_in_caches.append(list(videos))
        # print(videos_in_caches)


        # Placer une video dans un cache, par rapport à un endpoint,
        # ça sauve num_requests * saved_latency[cache, endpoint]

    # d[cle] = valeur

    with open("%s.greg" % filename, 'w') as f:
        f.write(str(problem_data.num_caches))
        f.write('\n')

        for (num_cache, videos_in_cache) in enumerate(videos_in_caches):
            # print(videos_in_cache)
            f.write("%d " % num_cache)
            f.write(' '.join(map(str, videos_in_cache)))
            f.write('\n')


def get_time_saved_per_video(cache, problem_data):
    time_saved_per_video = {}
    saved_latencies = problem_data.cache_to_endpoint_saved_latencies[cache]
    for info in saved_latencies:
        endpoint = info['endpoint']
        saved_latency = info['saved_latency']

        for data in problem_data.requests_for_endpoint[endpoint]:
            num_requests = data['num_requests']
            video_num = data['video_num']

            saved_time = num_requests * saved_latency
            if video_num in time_saved_per_video:
                time_saved_per_video[video_num] += saved_time
            else:
                time_saved_per_video[video_num] = saved_time
    # print(time_saved_per_video)
    return time_saved_per_video

def update_problem_data(video_num, cache_num, problem_data):
    # problem_data.cache_to_endpoint_saved_latencies

    for num_endpoint in range(problem_data.num_endpoints):
        current_latency = problem_data.best_ready_latency[num_endpoint]
        new_latency = problem_data.endpoint_to_cache_latencies[num_endpoint][cache_num]
        problem_data.best_ready_latency[num_endpoint] = min(new_latency, current_latency)

        for j in problem_data.endpoint_to_cache_latencies[num_endpoint].keys():
            latency = problem_data.endpoint_to_cache_latencies[num_endpoint][j]

            info = {"saved_latency": problem_data.best_ready_latency[num_endpoint] - latency,
                    "endpoint": num_endpoint}

            if cache_num in problem_data.cache_to_endpoint_saved_latencies:
                problem_data.cache_to_endpoint_saved_latencies[cache_num].append(info)
            else:
                problem_data.cache_to_endpoint_saved_latencies[cache_num] = [info]


def get_time_saved_per_video2(cache, problem_data):
    time_saved_per_video = get_time_saved_per_video(cache, problem_data)
    return {video: saved/problem_data.video_sizes[video] ** 0.3
            for (video, saved) in time_saved_per_video.items()}



def solve_problem2(filename):
    print(filename)

    problem_data = Data("../Data/%s.in" % filename)

    videos_in_caches = []
    for cache in range(problem_data.num_caches):

        time_saved_per_video = get_time_saved_per_video(cache, problem_data)
        sorted_videos = sorted(time_saved_per_video.items(), key=operator.itemgetter(0))
        # print(sorted_videos)

        videos = set()
        remaining_space = problem_data.cache_size
        for (video_num, saved_time) in sorted_videos:
            video_size = problem_data.video_sizes[video_num]
            if video_size < remaining_space:
                videos.add(video_num)
                update_problem_data(video_num, cache, problem_data)
                remaining_space -= video_size



        videos_in_caches.append(list(videos))


    with open("%s.greg" % filename, 'w') as f:
        f.write(str(problem_data.num_caches))
        f.write('\n')

        for (num_cache, videos_in_cache) in enumerate(videos_in_caches):
            # print(videos_in_cache)
            f.write("%d " % num_cache)
            f.write(' '.join(map(str, videos_in_cache)))
            f.write('\n')


# lalal
def solve_problem3(filename):
    print(filename)

    problem_data = Data("../Data/%s.in" % filename)

    # Trier paires (cache, video) en fonction du temps economisé

    videos_in_caches = []
    all_cached_videos = set()
    for cache in range(problem_data.num_caches):

        time_saved_per_video = get_time_saved_per_video(cache, problem_data)
        sorted_videos = sorted(time_saved_per_video.items(), key=operator.itemgetter(0))
        # print(sorted_videos)

        videos = set()
        remaining_space = problem_data.cache_size
        # Try to cache unchached videos
        for (video_num, saved_time) in sorted_videos:
            video_size = problem_data.video_sizes[video_num]
            if video_size < remaining_space and video_num not in all_cached_videos:
                videos.add(video_num)
                update_problem_data(video_num, cache, problem_data)
                all_cached_videos.add(video_num)
                remaining_space -= video_size

        # Fill the remaining space
        for (video_num, saved_time) in sorted_videos:
            video_size = problem_data.video_sizes[video_num]
            if video_size < remaining_space and video_num not in videos:
                videos.add(video_num)
                remaining_space -= video_size

        videos_in_caches.append(list(videos))

    with open("%s.greg" % filename, 'w') as f:
        f.write(str(problem_data.num_caches))
        f.write('\n')

        for (num_cache, videos_in_cache) in enumerate(videos_in_caches):
            # print(videos_in_cache)
            f.write("%d " % num_cache)
            f.write(' '.join(map(str, videos_in_cache)))
            f.write('\n')

def solve_problem4(filename):
    print(filename)

    problem_data = Data("../Data/%s.in" % filename)

    # Trier paires (cache, video) en fonction du temps economisé

    videos_in_caches = []
    all_cached_videos = set()
    for cache in range(problem_data.num_caches):

        time_saved_per_video = get_time_saved_per_video2(cache, problem_data)
        sorted_videos = sorted(time_saved_per_video.items(), key=operator.itemgetter(0))
        # print(sorted_videos)

        videos = set()
        remaining_space = problem_data.cache_size
        # Try to cache uncached videos
        for (video_num, saved_time) in sorted_videos:
            video_size = problem_data.video_sizes[video_num]
            if video_size < remaining_space and video_num not in all_cached_videos:
                videos.add(video_num)
                all_cached_videos.add(video_num)
                remaining_space -= video_size

        # Fill the remaining space
        for (video_num, saved_time) in sorted_videos:
            video_size = problem_data.video_sizes[video_num]
            if video_size < remaining_space and video_num not in videos:
                videos.add(video_num)
                remaining_space -= video_size

        videos_in_caches.append(list(videos))

    print("Saving file %s.greg" % filename)
    with open("%s.greg" % filename, 'w') as f:
        f.write(str(problem_data.num_caches))
        f.write('\n')

        for (num_cache, videos_in_cache) in enumerate(videos_in_caches):
            # print(videos_in_cache)
            f.write("%d " % num_cache)
            f.write(' '.join(map(str, videos_in_cache)))
            f.write('\n')



def should_save_video2(video_num, video_size, sorted_videos, time_saved_per_video, all_cached_videos):
    if video_num not in all_cached_videos:
        return True

    best_video = sorted_videos[0][0]
    best_time = time_saved_per_video[best_video]
    if time_saved_per_video[video_num]/best_time > 0.8:
        return True

    return False

def solve_problem5(filename):
    print(filename)

    problem_data = Data("../Data/%s.in" % filename)

    # Trier paires (cache, video) en fonction du temps economisé

    videos_in_caches = []
    all_cached_videos = set()
    for cache in range(problem_data.num_caches):

        time_saved_per_video = get_time_saved_per_video(cache, problem_data)
        sorted_videos = sorted(time_saved_per_video.items(), key=operator.itemgetter(0))
        # print(sorted_videos)

        videos = set()
        remaining_space = problem_data.cache_size

        # Try to cache unchached videos
        for (video_num, saved_time) in sorted_videos:
            video_size = problem_data.video_sizes[video_num]
            should_save = should_save_video2(video_num, video_size, sorted_videos, time_saved_per_video, all_cached_videos)

            if video_size < remaining_space and should_save:
                videos.add(video_num)
                all_cached_videos.add(video_num)
                remaining_space -= video_size

        # Fill the remaining space
        for (video_num, saved_time) in sorted_videos:
            video_size = problem_data.video_sizes[video_num]
            if video_size < remaining_space and video_num not in videos:
                videos.add(video_num)
                remaining_space -= video_size

        videos_in_caches.append(list(videos))

    with open("%s.greg" % filename, 'w') as f:
        f.write(str(problem_data.num_caches))
        f.write('\n')

        for (num_cache, videos_in_cache) in enumerate(videos_in_caches):
            # print(videos_in_cache)
            f.write("%d " % num_cache)
            f.write(' '.join(map(str, videos_in_cache)))
            f.write('\n')


# Faire update de cache_to_endpoint_saved_latencies

# TODO: garder best latency pour (endpoint, video)

def solve_problems_with_algo(algo):
    algo("me_at_the_zoo")
    algo("videos_worth_spreading")
    algo("trending_today")
    algo("kittens")

# solve_problems_with_algo(solve_problem)
# solve_problems_with_algo(solve_problem2)
# solve_problems_with_algo(solve_problem3)
# solve_problems_with_algo(solve_problem4)
solve_problems_with_algo(solve_problem2)
