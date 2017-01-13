Usage:

Edit `config.ini` with your `username`, `password`, `forum_number`, and/or `[forum URL]`.

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ python
    >>> from phpbb_poster import new_topic
    >>> subj = "Pull request description"
    >>> msg = """
    My pull request does this.

    Stuff used to be like that.
    They don't think it be like [b]it is[/b], but it [i]do[/i].
    """
    >>> new_topic(subj, msg)
