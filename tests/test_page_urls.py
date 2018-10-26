# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from __future__ import print_function  # Use print() instead of print
from flask import url_for


def test_page_urls(client):
    # Visit home page
    response = client.get('/', follow_redirects=True)
    assert response.status_code==200

    # Try to login with wrong email
    response = client.post(url_for('user.login'), follow_redirects=True,
                           data=dict(email='non_member@example.com', password='Password1'))
    assert response.status_code==200
    assert b"You have signed in successfully" not in response.data
    assert b"Sign In to your account" in response.data

    # Login as user and visit User page
    response = client.post(url_for('user.login'), follow_redirects=True,
                           data=dict(email='member@example.com', password='Password1'))
    assert response.status_code==200
    assert b"You have signed in successfully" in response.data
    assert b"Sign In to your account" not in response.data

    response = client.get(url_for('main.member_page'), follow_redirects=True)
    assert response.status_code==200
    assert b"Traffic" in response.data

    # Edit User Profile page
    response = client.get(url_for('main.user_profile_page'), follow_redirects=True)
    assert response.status_code==200
    assert b"User Profile" in response.data
    assert b"First name" in response.data
    assert b"Member" in response.data

    response = client.post(url_for('main.user_profile_page'), follow_redirects=True,
                           data=dict(first_name='User', last_name='User'))
    assert b"User Profile" in response.data
    assert b"First name" in response.data
    assert b"Member" not in response.data

    response = client.get(url_for('main.member_page'), follow_redirects=True)
    assert response.status_code==200
    assert b"User Profile" not in response.data
    assert b"First name" not in response.data
    assert b"Traffic" in response.data

    # Logout
    response = client.get(url_for('user.logout'), follow_redirects=True)
    assert response.status_code==200
    assert b"You have signed out successfully." in response.data

    # Login as admin and visit Admin page
    response = client.post(url_for('user.login'), follow_redirects=True,
                           data=dict(email='admin@example.com', password='Password1'))
    assert response.status_code==200
    assert b"You have signed in successfully" in response.data
    assert b"Sign In to your account" not in response.data

    response = client.get(url_for('main.admin_page'), follow_redirects=True)
    assert response.status_code==200
    print(url_for('main.admin_page'))
    assert b"System Users" in response.data
    assert b"Create User" in response.data

    # Logout
    response = client.get(url_for('user.logout'), follow_redirects=True)
    assert response.status_code==200
    assert b"You have signed out successfully." in response.data
