AWS CDK Reference Quick Search
==============================================================================


What is this?
------------------------------------------------------------------------------
I create an `Alfred Workflow <https://www.alfredapp.com/workflows/>`_ framework called `Full Text Search Anything <https://github.com/MacHu-GWU/afwf_fts_anything-project>`_. You can bring your own json data, define how you gonna index it, then use Alfred Workflow to search it.

**This project allows you to quickly search and browse** `AWS CDK reference documents <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-construct-library.html>`_. It automates the creation of the "your own json data" for document searching.

.. image:: https://user-images.githubusercontent.com/6800411/232178797-17594a06-c3f0-4b4c-b433-0423eca22cdd.gif


How it Work?
------------------------------------------------------------------------------
The `build_data.py <./build_data.py>`_ is a crawler that scrape information from https://docs.aws.amazon.com/cdk/api/v2/, and generate a json file like this::

    [
        {
            "service": "aws_cdk",
            "object": "Package Overview",
            "url": "https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk/README.html"
        },
        {
            "service": "aws_cdk",
            "object": "Annotations",
            "url": "https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk/Annotations.html"
        },
        ...
    ]

Just run the following script, it will generate the data file and setting file on Git repo root directory.

.. code-block:: bash

    pip3 install -r requirements.txt
    python3 build_data.py


How to Install?
------------------------------------------------------------------------------
**Dependencies**:

    You have to install `the Full-Text-Search Anything Alfred Workflow <https://github.com/MacHu-GWU/afwf_fts_anything-project>`_, make sure you read the document there and successfully configured the sample IMDB top 250 movies dataset working.

**The automate way**:

    We have a `installation script <./install.py>`_, so just do:

    .. code-block:: bash

        python3 -c "$(curl -fsSL https://raw.githubusercontent.com/MacHu-GWU/alfred-cdk-ref/main/install.py)"

**The manual way**:

    You can also download the dataset directly from `Release <https://github.com/MacHu-GWU/alfred-cdk-ref/releases>`_. Just Download ``cdk-data.zip``, extract it in ``${HOME}/.alfred-afwf/afwf_fts_anything/``. Follow Alfred Workflow Config instruction in https://github.com/MacHu-GWU/afwf_fts_anything-project

**Configure Full-Text-Search Alfred Workflow**

.. image:: https://user-images.githubusercontent.com/6800411/232178692-fd80540f-4078-4419-8c5e-f0c98da55d1a.png

.. image:: https://user-images.githubusercontent.com/6800411/232178693-41a21de8-1f28-489f-bb91-e78f93271caf.png
