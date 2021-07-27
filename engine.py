import psycopg2
import random

conn = psycopg2.connect(
   database="dvk6lrjqokq93", 
   user='zubvkjwkjfqnni', 
   password='efa884e7ff57cf3f2c11301bea345029c62890dd72cac8c743057a4a910184f0', 
   host='ec2-44-194-112-166.compute-1.amazonaws.com', 
   port= '5432'
)

conn.autocommit = True
cursor = conn.cursor()

def get_manager(new_hire):
    cursor.execute(f"select * from org_chart where name like (select reports_to from org_chart where name like '{new_hire}');")
    return cursor.fetchall()

def get_teammates(new_hire):
    try:
        manager = get_manager(new_hire)[0][1]
        cursor.execute(f"select * from org_chart where reports_to like '{manager}';")
        return cursor.fetchall()
    except IndexError:
        return None

def get_subordinates(new_hire):
    cursor.execute(f"select * from org_chart where reports_to like '{new_hire}';")
    return cursor.fetchall()

# returns single name
def get_manager_of_manager(new_hire):
    cursor.execute(f"select reports_to from org_chart where name like (select reports_to from org_chart where name like '{new_hire}');")
    try:
        return cursor.fetchall()[0][0]
    except:
        return None

def get_all_managers(new_hire):
    manager_of_manager = get_manager_of_manager(new_hire)
    cursor.execute(f"select * from org_chart where reports_to like '{manager_of_manager}';")
    return cursor.fetchall()

def get_sibling_team_members(new_hire):
    all_managers = [f"\'{i[1]}\'" for i in get_all_managers(new_hire)]
    all_managers = ",".join(all_managers)
    manager = get_manager(new_hire)
    try:
        cursor.execute(f"select * from org_chart where reports_to in ({all_managers}) and reports_to != '{manager[0][1]}';")
        return cursor.fetchall()
    except:
        return None

def get_random(limit):
    cursor.execute(f"select * from org_chart order by random() limit {limit};")
    return cursor.fetchall()


def recommend(user):
    recommendation = []

    slot1 = get_manager(user)
    slot2 = get_teammates(user)
    slot3 = get_subordinates(user)
    slot4 = get_manager_of_manager(user)
    slot5 = get_all_managers(user)
    slot6 = get_sibling_team_members(user)
    slot7 = get_random(5)

    if slot1 != []:
        recommendation.append(slot1[0][1])
    if slot2 != None:
        for i in slot2[:5]:
            recommendation.append(i[1])
    if slot3 != []:
        for i in slot3[:5]:
            recommendation.append(i[1])
    if slot4 != None:
        recommendation.append(slot4)
    if slot5 != []:
        for i in slot5[:5]:
            recommendation.append(i[1])
    if slot6 != None:
        for i in slot6[:5]:
            recommendation.append(i[1])
    # if len(recommendation) < 22:
    for i in slot7[:5]:
        recommendation.append(i[1])
    try:
        recommendation.remove(user)
    except:
        pass
    recommendation = list(set(recommendation))
    return random.choices(recommendation, k=5) 

# print(get_manager("lisa utzschneider"))
# print(get_teammates("lisa utzschneider"))
# print(get_subordinates('lisa utzschneider'))
# print(get_manager_of_manager('lisa utzschneider'))
# print(get_all_managers('lisa utzschneider'))
# print(get_sibling_team_members('lisa utzschneider'))