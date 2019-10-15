from API import access_token, v
import csv
import requests
from time import sleep
import collections

educational_programs = ['ES4', 'AMI4', 'IR4', 'J4']
common_groups_number = 35
groups = ["hse_university", "thevyshka", "hse_case_school", "iqhse", "hseofficial"]


def read_students(program):
    path = 'C:/Users/User/PycharmProjects/Culture_Centre/students/{program}.csv'.format(program=program)
    students = list()
    with open(path, 'r', encoding='utf-8') as file_program:
        reader = csv.reader(file_program)
        for line in reader:
            n, full_name = line[0].split(';')
            last_name, first_name, patronymic = full_name.split()[:3]
            students.append(first_name + ' ' + last_name)
    return students


def find_ids(student, groups_search):
    ids = list()
    for group in groups_search:
        path_to_groups = 'C:/Users/User/PycharmProjects/Culture_Centre/groups/{group}.csv'.format(group=group)
        with open(path_to_groups, 'r', encoding='utf-8') as file_group:
            reader = csv.reader(file_group)
            for line in reader:
                id, full_name = line
                if full_name == student:
                    ids.append(id)
    return ids


def get_friends_info(id):  # dict() [full_name] = id
    global access_token, v
    friends_info = dict()
    params = {
        'access_token': access_token,
        'v': v,
        'user_id': id,
        'fields': 'is_closed'
    }
    response = requests.get('https://api.vk.com/method/friends.get', params=params).json()
    sleep(0.334)
    if response.get('error'):
        print(response['error']['error_msg'])
        return friends_info
    for item in response['response']['items']:
        if not item.get('deactivated'):
            if not item['is_closed']:
                full_name = item['first_name'] + ' ' + item['last_name']
                friends_info[full_name] = item['id']
    return friends_info


def find_pages(students, groups_search, friends_in_common=3):  # dict() [full_name] = id
    print('searhing for pages...')
    students = set(students)
    students_covered = set()
    students_pages = dict()
    for student in students:
        ids = find_ids(student, groups_search)
        friends_intersections = list()
        common_friends = dict()
        for id_st in ids:
            friends_info = get_friends_info(id_st)
            common = set(friends_info.keys()).intersection(students)
            common_friends[id_st] = dict()
            for common_full_name in common:
                common_friends[id_st][common_full_name] = friends_info[common_full_name]
            friends_intersections.append(len(common))
        if friends_intersections:
            likable = max(zip(friends_intersections, ids))
            if likable[0] > friends_in_common:
                students_pages[student] = likable[1]
                students_covered.add(student)
                friends = common_friends[likable[1]]
                for friend_full_name, friend_id in friends.items():
                    students_pages[friend_full_name] = friend_id
                    students_covered.add(friend_full_name)
        print(round(len(students_covered) / len(students) * 100, 3), '% covered')
    print('final coverage', round(len(students_covered) / len(students) * 100, 3), '%', len(students_covered), 'students')
    return students_pages


def get_groups(id):
    global access_token, v
    groups = list()
    params = {
        'access_token': access_token,
        'v': v,
        'user_id': id,
        'extended': 1,
    }
    response = requests.get('https://api.vk.com/method/groups.get', params=params).json()
    sleep(0.334)
    for item in response['response']['items']:
        groups.append(item['name'])
    return groups


if __name__ == '__main__':
    student_groups = dict()
    for program in educational_programs:
        students = read_students(program)
        pages = find_pages(students, groups)
        print('receiving groups...')
        i = 0
        for full_name, id in pages.items():
            i += 1
            student_groups[full_name] = get_groups(id)
        print('students covered at {program} {0}'.format(i, program=program))
    print('students overall: {0}, with the number of unique groups: {1}'.format(len(student_groups.keys()),
                                                                                len(student_groups.values())))

    student_vectors = []
    values = []
    for ar1 in list(student_groups.values()):
        for el in ar1:
            values.append(el)
    groups_counter = collections.Counter(values)
    print('most common groups:')
    print(*groups_counter.most_common(common_groups_number), sep='\n')
    for gr, n in groups_counter.most_common(common_groups_number):
        student_vectors.append(gr)
    for program in educational_programs:
        path_to_students = 'C:/Users/User/PycharmProjects/Culture_Centre/students/{program}_data.csv'.format(program=program)
        print(path_to_students)
        with open(path_to_students, 'w', encoding='cp1251') as file_to_students:
            print('recording...')
            writer = csv.writer(file_to_students)
            writer.writerow(['full_name', *student_vectors])
            for student, communities in student_groups.items():
                vector = list()
                for community in student_vectors:
                    if community not in communities:
                        vector.append(0)
                    else:
                        vector.append(1)
                writer.writerow([student, *vector])
            print('completed file {program}'.format(program=program))