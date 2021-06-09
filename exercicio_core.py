from __future__ import division
from collections import Counter, defaultdict

users = [
    { "id": 0, "name": "Hero" },
    { "id": 1, "name": "Dunn" },
    { "id": 2, "name": "Sue" },
    { "id": 3, "name": "Chi" },
    { "id": 4, "name": "Thor" },
    { "id": 5, "name": "Clive" },
    { "id": 6, "name": "Hicks" },
    { "id": 7, "name": "Devin" },
    { "id": 8, "name": "Kate" },
    { "id": 9, "name": "Klein" }
]

friendships = [
     (0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
    (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)
]

interests = [
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
    (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
    (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
    (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"),
    (3, "statistics"), (3, "regression"), (3, "probability"),
    (4, "machine learning"), (4, "regression"), (4, "decision trees"),
    (4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
    (5, "Haskell"), (5, "programming languages"), (6, "statistics"),
    (6, "probability"), (6, "mathematics"), (6, "theory"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
    (7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
    (8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"),
    (9, "Java"), (9, "MapReduce"), (9, "Big Data")
]

salaries_and_tenures = [
    (83000, 8.7), (88000, 8.1),
    (48000, 0.7), (76000, 6),
    (69000, 6.5), (76000, 7.5),
    (60000, 2.5), (83000, 10),
    (48000, 1.9), (63000, 4.2)
]

# add um par firiends: [] a cada dict em users
for user in users:
    user["friends"] = []

for i, j in friendships:
    users[i]["friends"].append(users[j]) # add i como um amigo de j
    users[j]["friends"].append(users[i]) # add j como um amigo de i

def number_of_friends(user):
    """quantos amigos o usuario tem"""
    return len(user["friends"])

total_connections = sum(number_of_friends(user) for user in users)

num_user = len(users) # tamanho da lsta de usuarios
avg_connections = total_connections/num_user

# cria uma lista (user_id_number_of_friends)
num_friends_by_id = [(user["id"], number_of_friends(user))
        for user in users]

sorted(num_friends_by_id,
       key= lambda userid_numfriends: userid_numfriends[1],
       reverse=True)

def friends_of_firend_ids_bad(user):
    # foaf abreviacao de friend de friend
    return [
        foaf["id"]
        for friend in user["friends"] # para cada amigo de usuario
        for foaf in friend["friends"] # pega cada _their_friends
    ]

print(friends_of_firend_ids_bad(users[0]))

def not_the_same(user, other_user):
    """dois usuarios nao sao a mesma pessoa se possuem ids diferentes"""
    return user["id"] != other_user["id"]

def not_friends(user, other_user):
    """other_user não é um amigo se nao esta em user["friends"];
    istoé, se é not_the_same com todas a pessoa em user["friends"]"""
    return all(not_the_same(friend, other_user)
            for friend in user["friends"])

def friends_of_friend_ids(user):
    return Counter(foaf["id"]
        for friend in user["friends"] # para cada um dos meus amigos
        for foaf in friend["friends"] # que contam *their* amigos
        if not_the_same(user, foaf) # que nao sejam eu
        and not_friends(user, foaf) # e que nao são os meus
    )

print(friends_of_friend_ids(users[0])) 
print(friends_of_friend_ids(users[3])) # Counter({0:2, 5: 1})

def data_scientists_who_like(target_interest):
    """usuarios com mesmo interesse"""
    return [user_id
        for user_id, user_interest in interests
        if user_interest == target_interest
    ]

# as chaves aõ interesses, os valores são listas de user_ds com inteerests
user_ids_by_interest = defaultdict(list)

for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)


# as chaves são user_ids, os valores são as listas de interests para aqueel user_id
# cria um dict com chave id_user e values os interesses
interests_by_user_id = defaultdict(list)
for user_id, interest in interests:
    interests_by_user_id[user_id].append(interest)

# print(interests_by_user_id)

def most_common_interests_with(user):
    return Counter(interested_user_id
        for interest in interests_by_user_id[user["id"]]
        for interested_user_id in user_ids_by_interest[interest]
        if interested_user_id != user["id"]
    )

print(most_common_interests_with(users[0]))

# slario e experiencia
# as chaves são os anos, os valores são as listas dos salarios para cada ano
salary_by_tenue = defaultdict(list)

for salary, tenue in salaries_and_tenures:
    salary_by_tenue[tenue].append(salary)

# as chaves são os anos, cada valor é a média salarial para aquele ano
average_salary_by_tenue = {
    tenue: sum(salaries)/len(salaries)
    for tenue, salaries in salary_by_tenue.items()
}

# print(average_salary_by_tenue)

def tenue_bucket(tenue):
    if tenue < 2:
        return "less than two"
    elif tenue < 5:
        return "between two and five"
    else:
        return "more than five"

# as chaves são agrupamentos dos casos, os valores são as listas
# dos salarios para aquele agrupamento
salary_by_tenue_bucket = defaultdict(list)
for salary, tenue in salaries_and_tenures:
    bucket = tenue_bucket(tenue)
    salary_by_tenue_bucket[bucket].append(salary)

# print(salary_by_tenue_bucket)

# as chaves são agrupamentos dos casos, os valores são
# a média salarial para aquelea grupamento
# calculo da media salarial
average_salary_by_bucket = {
    tenue_bucket: sum(salaries)/len(salaries)
    for tenue_bucket, salaries in salary_by_tenue_bucket.items()
}

print(average_salary_by_bucket)

# topicos de interesse

words_and_counts = Counter(
    word
    for user, interest in interests
    for word in interest.lower().split()
)

# print(words_and_counts)

for word, count in words_and_counts.most_common():
    if count > 1:
        print(word, count)