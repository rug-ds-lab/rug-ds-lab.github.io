# RUG DS Website
This repository is home to the static website used over on rug-ds-lab.github.io.
The website is split into two repositories, one for the content (this repository)
and the other for the theme. Deployment is done automatically using GitHub Actions
and changes should therefore first be applied in the `dev` branch, followed by
a pull into main.

# How-To
Due to some Jekyll restrictions, people will have to be added to multiple different
parts of the website depending on whether they have publications, supervise 
projects. It is therefore important that steps are followed for each applicable
section of the website for that person.

## Publications
Publications are automatically fetched from ORCID at each rebuild of the website.
To add a new member to the publications page, the following steps are to be 
followed:

1. Add a new file `[firstname_lastname].md` with in the front matter a field called `orcid`, which is the 8 digit orcid ID of that person.
2. Pull changes into `main` branch.

This will fetch the latest publications for all members, now including the 
newly added member

## People
People are added to the website the same way as publications.

- Add a new file `[firstname_lastname].md` for that person, containing the following fields in the front matter:
    - `layout: person` (required)
    - `name` (required)
    - `level: [faculty/member/student/alumni]` (required)
    - `academic_status` (required)
    - `picture` (path)
    - `email`
    - `research` (list)
    - `room`
  
  Pictures are to be stored in the `_people/pictures` directory
- Pull changes into `main` branch.

The newly added person will now be visible in their respective section on the 
People page.

## Education
Courses taught by the research group are automatically put into tables, with
only the current year being shown my default. Generation of these tables is done
automatically and the current education year is defined by the most recent course
available in the collection `courses`.

- Firstly add a new folder for the applicable academic year in the `_courses`
folder. 
- Then add add a new file for the new course with a suitable name. The name of
this file will dictate what the URL will show, so be mindful of that.
- In the frontmatter, the following fields should be added:
    - `title`: name of the course (required)
    - `level`: level of the course (required)
    - `instructor`: person giving the course (required)
    - `year`: academic year in which the course is given in the format 
    `[year]-[year+1]` (required)

If courses for a new academic year are added to the `courses` collection, older
courses will automatically be cascaded down into `previous years` on the website.

## Projects
The projects that the research group offers are added as follows:

- Add a new list entry in the `_data/projects.yml` containing the following 
fields
    - `title`: project title (required)
    - `supervisors`: array of supervisors (required)
    - `available`: current availability boolean (required)
    - `date`: Added date \[yyyy-mm-dd\] (required)
    - `type`: project type/level \[spp/bachelor/master/colloquium/internship\] 
    (required)
    - `description`: description of the project (required)

# Filters
## Publication filters
add a file `_filters/[firstname-lastname.md]` to add a filter which publications can be filtered by. Then add the following fields in the frontmatter:
- `layout: publication` (required)

depending on the filter type, add **one** of the following:
- year filter: `filter_year: [year]`
- person filter: `filter_author: [Capitalized Name]`
- type filter: `filter_type: [bibtex type]`

## Project filters
To be able to filter projects by a supervisor, add a file to either `_projects/supervisors` if you want to filter by supervisor or `_projects/type` if you want to filter by type.

If the filter is by supervisor, add the following:
- `layout: project` (required)
- `title: [capitalized name]` (required)
- `filter_type: supervisor` (required)

If the filter is a type filer, add the following:
- `layout: type` (required)
- `title: [capitalized type name]` (required)
- `type: [spp/bachelor/master/colloquium/internship]` (required)
- `filter_type: type` (required)

# News
News articles can easily be added by adding a Markdown or HTML file in the `_news` folder with a fitting name. The frontmatter should contain the following:

- `layout: default` (required)
- `title: [desired title]` (required)
- `date: [date in yyyy-mm-dd]` (required)

The content following the front matter will be rendered on a new news entry in the `/news` page.