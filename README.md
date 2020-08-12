# Hackers Assistance

This is a repository for automatic programs helped work easily when I worked as hackers assistant in Hackers. I can reduce a lot of time that spent on other important matters through this repo. Program list is as follows.

1. Update the number of student applied classes
2. Check students' comments 

**Requirements**
- Hackers assistance ID and PASSWORD  
    https://www.hackers.ac/teachers/index.php
- Notion page url and token_v2  
    [How to get token_v2](https://github.com/TooTouch/notionist)

# 1. Update the number of student applied classes

**Run**
```bash
python students.py --id=YOUR_ID --pwd=YOUR_PASSWORD
```

**Result**
- students.csv
    Features | Description
    ---|---
    title | class name (group)
    name | class name (full)
    class_time | class time
    onoff | 1. on-line 2. off-line
    nb_students | the number of student

- students_stat.csv
    - Getting sum of the number of student by title in students.csv

    Features | Description
    ---|---
    title | class name (group)
    class_time | class time
    nb_students | the number of student



# 2. Check students' comments

**Run**

I use github action which runs periodically comments.py. If you want to know how to set options, you can see [here](https://github.com/TooTouch/Hackers-Assistance/blob/master/.github/workflows/python-package.yml).

**Result**
- Dataframe Description

    Features | Description
    ---|---
    title | post title
    name | publisher name
    category | 1. teacher 2. student
    class_name | class name (full-name)
    date | published date
    nb_comment | the number of comment
    url  | post url

- Notion Collection(Table)
    ![comments](https://user-images.githubusercontent.com/37654013/89047569-901cac80-d389-11ea-8b35-8af1fb631945.png)
