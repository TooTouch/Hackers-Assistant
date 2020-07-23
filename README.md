# Hackers Assistance

This is a repository for automatic programs helped works easily during hackers assistance. I can reduce a lot of time that spent on other important matters through this repo. Program list is as follows.

1. Update the number of student applied classes
2. Check students' comments 


# 1. Update the number of student applied classes

**How to run**
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

**How to run**
```bash
python comments.py --id=YOUR_ID --pwd=YOUR_PASSWORD \
                    --token_v2=YOUR_token_v2 --url=NOTION_URL
```

**Result**
- Notion collection(table)

    Features | Description
    ---|---
    title | post title
    name | publisher name
    category | 1. notice 2. question
    class_name | class name (full-name)
    date | published date
    nb_comment | the number of comment
    url  | post url