#!/usr/bin/env python3
"""
Definition of class SessionAuth
"""
from uuid import uuid4
from typing import TypeVar
from .auth import Auth
from models.user import User
from flask import request
from os import getenv


class SessionAuth(Auth):
    """ Implement Session Authorization protocol methods """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user with id user_id
        Args:
            user_id (str): user's user id
        Return:
            None if user_id is None or not a string
            Session ID in string format
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a user ID based on a session ID
        Args:
            session_id (str): session ID
        Return:
            user id or None if session_id is None or not a string
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def session_cookie(self, request=None):
        """
        Returns the session cookie from the request
        Args:
            request : request object containing cookies
        Return:
            the value of the cookie named by SESSION_NAME environment variable
        """
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)

    def current_user(self, request=None):
        """
        Return a user instance based on a cookie value
        Args:
            request : request object containing cookie
        Return:
            User instance or None if no valid session
        """
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return None
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes a user session
        Args:
            request : request object containing the session cookie
        Return:
            True if session was successfully deleted, False otherwise
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True

