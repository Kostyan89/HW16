import json
from models import User, Order, Offer
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

