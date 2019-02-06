# Scientific Wagtail

This repository contains the website, that I developed for my personal blog. The blog is based on [Wagtail CMS](https://wagtail.io) and includes the support of Markdown and MathJax. Comments to the blog posts are now done using [Disqus](https://disqus.com). The design is very simple and based on [Bootstrap](https://getbootstrap.com). I use minimum amount of Javascript since I do not have any experience in frontend development.

I'm planning to keep the repository updated to the latest versions Wagtail, Django, Bootstrap and other packages.


### Install

Clone this repository:

    git clone git@github.com:naitsok/scientific-wagtail.git


Create an environment and install Python packages:

    virtualenv env -p python3
    source env/bin/activate
    pip install -r requirements.txt


Configure your database or use the default for development. Use you favorite approach for local settings.

    nano scientific-wagtail/settings/dev.py
    nano scientific-wagtail/settings/production.py


Make migrations, create a user and run the development server:

    python manage.py migrate
    python manage.py createsuperuser
	python manage.py collectstatic
    python manage.py runserver
    
    
### Plans

I do not have specific plans yet for further development except keeping it up-to-date and adding features, that I need. For example, I might add StreamField support for a tool, such as Chem Draw, if I really need it and there is a good open source editor. 


### Changelog

##### Version 1.0.4
- Released 06.02.2019
- Features:
	- Sitemap.

##### Version 1.0.3
- Released 04.02.2019
- Features:
	- Blog page now has image with caption and table with caption blocks.
	- Minor design changes.

##### Version 1.0.2
- Released 03.02.2019
- Refactoring:
	- Moved all blocks for Wagtail stream field to one new Django app, sciwagblocks app.

##### Version 1.0.1
- Released 03.02.2019
- Features:
	- Table and table with caption blocks for Wagtail stream field.
	- The blocks are added to post page.

##### Version 1.0.0
- Released 04.01.2019. 
- Features: 
	- Custom User model, than can be extended if needed.
	- Markdown StreamField Block.
	- Standalone Equation StreamField Block.
	- Two-column StreamField Block.
	- Custom blockquote block with fields for author and source.
	- MathJax support.
	- Images and equations numbering.
	- Sidebar with post contents, figures and equations.
	- Post tags and categories.
	- Tag cloud and simple one-level categories.
	- Post Series. Post can contain child posts. In this case the post and its child posts are marked as "Series".
	- Pinned posts. You can pin specific posts on the front page.
	- Form page for e.g. contact forms.
    - Post archives.
    - Post search, filter by category, tag, date, author.
	- Comments via [Disqus](https://disqus.com).
 
