#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (
    unicode_literals,
    print_function
    )

import os
import random

from pydoc import (
    locate)
from config import (
    app_config)
from flask import (
    Flask,
    request,
    jsonify,
    redirect,
    url_for,  # Added url_for
    Blueprint,
    render_template)
from models import (
    system)
from logsdata import (
    logger)


def create_app(config_name):
    """Create App"""
    app = Flask(
        __name__,
        instance_relative_config=True
        )

    app.config.from_object(
        app_config[config_name])
    app.config.from_pyfile(
        'config.py')
    app.config['SECRET_KEY'] = "\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16"

    logger.info("Initialize System Queues")
    system.indexinit()

    """TODO: Migrate BP to MongoDB"""

    # Register AI-Core Blueprints
    from aicore import bp as aibp
    app.register_blueprint(aibp, url_prefix="/aicore")

    # Register Asterisk Blueprints
    from asterisk import bp as asteriskbp
    app.register_blueprint(asteriskbp, url_prefix="/asterisk")

    # Register User Data Blueprints
    import userdata
    # userdata.init()
    app.register_blueprint(userdata.bp, url_prefix="/contacts")

    # Add Users and Roles API Routes
    @app.route('/api/users', methods=['POST'])
    def add_user():
        try:
            data = request.get_json()
            # TODO: Implement user creation logic
            # For now, just return a mock response
            return jsonify({
                'username': data['username'],
                'role': data['role'],
                'status': data['status']
            }), 201
        except Exception as e:
            logger.error(f"Error adding user: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/roles', methods=['POST'])
    def add_role():
        try:
            data = request.get_json()
            # TODO: Implement role creation logic
            # For now, just return a mock response
            return jsonify({
                'name': data['roleName'],
                'permissions': data['permissions']
            }), 201
        except Exception as e:
            logger.error(f"Error adding role: {str(e)}")
            return jsonify({'error': str(e)}), 500

    # Register Case Data Blueprints
    from casedata import bp as casebp
    app.register_blueprint(casebp, url_prefix="/casedata")

    # Register Chatbot Blueprints
    from chatbot import bp as chatbp
    app.register_blueprint(chatbp, url_prefix="/chatbot")

    logger.info("Completed Blueprint Registration")

    # Default Route Index
    @app.route("/", methods=['GET'])
    def index():
        logger.info("Helpline Index Page")
        return render_template(
            'index.html', title="Helpline: AI Case Management System")

    # Login Route Index
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            # Placeholder for actual user authentication logic.
            # You should validate username and password here.
            # Example (if using Flask-Login):
            # from flask_login import login_user
            # user = User.query.filter_by(username=request.form.get('username')).first()
            # if user and user.check_password(request.form.get('password')):
            #     login_user(user, remember=request.form.get('remember'))
            #     logger.info(f"User {user.username} logged in successfully, redirecting to dashboard.")
            #     return redirect(url_for('dashboard'))
            # else:
            #     logger.warning("Login failed for user.")
            #     # You might want to flash a message here: flash('Invalid username or password')
            #     return render_template('login.html', title="Login: AI Case Management System", error="Invalid credentials")

            # For now, directly redirecting assuming login is successful.
            logger.info("Login attempt via POST, redirecting to dashboard.")
            return redirect(url_for('dashboard'))
        
        # For GET request
        logger.info("Helpline Login Page (GET)")
        return render_template(
            'login.html', title="Login: AI Case Management System")

    # Register Route Index
    @app.route("/register", methods=['GET'])
    def register():
        logger.info("Helpline Register Page")
        return render_template(
            'register.html', title="Register: AI Case Management System")

    # Dashboard Route
    @app.route("/dashboard", methods=['GET'])
    # @login_required  # Uncomment this line if you are using Flask-Login and the dashboard should be protected
    def dashboard():
        logger.info("Helpline Dashboard Page")
        # You can pass any necessary data to your dashboard template here
        return render_template('sneat/dashboard_content.html', title="Dashboard")

    # Call Data Route
    @app.route("/call-data", methods=['GET'])
    def call_data():
        logger.info("Helpline Call Data Page")
        return render_template('sneat/calldata/index.html', title="Call Data")

    # Case Data Route
    @app.route("/case-data", methods=['GET'])
    def case_data():
        logger.info("Helpline Case Data Page")
        return render_template('sneat/casedata/case_data_content.html', title="Case Data")

    # AI Services Route
    @app.route("/ai-services", methods=['GET'])
    def ai_services():
        logger.info("Helpline AI Services Page")
        return render_template('sneat/aicore/index.html', title="AI Services")

    # Users & Roles Route
    @app.route("/users-roles", methods=['GET'])
    def users_roles():
        logger.info("Helpline Users & Roles Page")
        return render_template('sneat/contacts/users_roles_content.html', title="Users & Roles")

    # System Services Route
    @app.route("/system-services", methods=['GET'])
    def system_services():
        logger.info("Helpline System Services Page")
        return render_template('sneat/systemservices/system_services_content.html', title="System Services")

    # Chatbot Route
    @app.route("/chatbot", methods=['GET'])
    def chatbot():
        logger.info("Helpline Chatbot Page")
        return render_template('sneat/chatbot/chatbot_content.html', title="Chatbot")

    # Documentation Route
    @app.route("/documentation", methods=['GET'])
    def documentation():
        logger.info("Helpline Documentation Page")
        return render_template('sneat/documentation/documentation_content.html', title="Documentation")

    # Contacts Route
    @app.route("/contacts", methods=['GET'])
    def contacts():
        logger.info("Helpline Contacts Page")
        return render_template('sneat/contacts/contacts_content.html', title="Contacts")

    # Unified Data Route - Routes to appropriate blueprint based on filename
    @app.route("/data/<filename>", methods=['POST'])
    def unified_data(filename):
        logger.debug(f"Unified Data Route: {filename}")
        
        try:
            data = {}
            x = request.get_json()
            if 'next' not in x:
                x['next'] = False
            if 'prev' not in x:
                x['prev'] = False

            # Provide mock data based on filename
            mock_data = {
                # Call Data
                'call_data': {
                    'success': True,
                    'message': 'Call Data loaded successfully',
                    'data': {
                        'total_calls': 1250,
                        'active_calls': 45,
                        'avg_duration': '5m 32s',
                        'satisfaction_rate': 94.2,
                        'recent_calls': [
                            {'id': 'C001', 'duration': '3m 45s', 'status': 'completed'},
                            {'id': 'C002', 'duration': '7m 12s', 'status': 'active'},
                            {'id': 'C003', 'duration': '2m 18s', 'status': 'completed'}
                        ]
                    }
                },
                'call_analytics': {
                    'success': True,
                    'message': 'Call Analytics loaded successfully',
                    'data': {
                        'hourly_trends': [45, 52, 38, 61, 78, 89, 95, 87, 76, 65, 58, 49],
                        'daily_trends': [234, 256, 198, 312, 289, 345, 298],
                        'top_agents': ['Agent A', 'Agent B', 'Agent C'],
                        'call_types': {'Support': 45, 'Sales': 30, 'Inquiry': 25}
                    }
                },
                'call_reports': {
                    'success': True,
                    'message': 'Call Reports loaded successfully',
                    'data': {
                        'reports': [
                            {'name': 'Daily Summary', 'date': '2024-01-01', 'status': 'ready'},
                            {'name': 'Weekly Analysis', 'date': '2024-01-07', 'status': 'processing'},
                            {'name': 'Monthly Report', 'date': '2024-01-31', 'status': 'ready'}
                        ]
                    }
                },
                
                # Case Data
                'case_data': {
                    'success': True,
                    'message': 'Case Data loaded successfully',
                    'data': {
                        'total_cases': 890,
                        'open_cases': 156,
                        'resolved_cases': 734,
                        'avg_resolution_time': '2.3 days',
                        'recent_cases': [
                            {'id': 'CS001', 'priority': 'High', 'status': 'Open'},
                            {'id': 'CS002', 'priority': 'Medium', 'status': 'In Progress'},
                            {'id': 'CS003', 'priority': 'Low', 'status': 'Resolved'}
                        ]
                    }
                },
                'case_management': {
                    'success': True,
                    'message': 'Case Management loaded successfully',
                    'data': {
                        'workflows': ['New Case', 'In Progress', 'Under Review', 'Resolved'],
                        'assignments': {'Agent A': 12, 'Agent B': 8, 'Agent C': 15},
                        'priorities': {'High': 23, 'Medium': 45, 'Low': 88}
                    }
                },
                'case_analytics': {
                    'success': True,
                    'message': 'Case Analytics loaded successfully',
                    'data': {
                        'resolution_times': [1.2, 2.1, 3.5, 1.8, 2.9, 2.3, 1.7],
                        'case_volume': [45, 52, 38, 61, 78, 89, 95],
                        'satisfaction_scores': [4.2, 4.5, 4.1, 4.3, 4.6, 4.4, 4.2]
                    }
                },
                
                # AI Services
                'ai_services': {
                    'success': True,
                    'message': 'AI Services loaded successfully',
                    'data': {
                        'services': [
                            {'name': 'Transcription', 'status': 'active', 'accuracy': 95.2},
                            {'name': 'Translation', 'status': 'active', 'accuracy': 92.8},
                            {'name': 'Classification', 'status': 'active', 'accuracy': 89.5}
                        ],
                        'total_requests': 15420,
                        'success_rate': 96.8,
                        'avg_response_time': '1.2s'
                    }
                },
                'transcription': {
                    'success': True,
                    'message': 'Transcription service loaded successfully',
                    'data': {
                        'total_transcriptions': 8234,
                        'accuracy_rate': 95.2,
                        'languages': ['English', 'Spanish', 'French', 'German'],
                        'recent_files': ['audio_001.wav', 'audio_002.wav', 'audio_003.wav']
                    }
                },
                'translation': {
                    'success': True,
                    'message': 'Translation service loaded successfully',
                    'data': {
                        'total_translations': 5678,
                        'supported_languages': 12,
                        'accuracy_rate': 92.8,
                        'popular_pairs': ['EN-ES', 'ES-EN', 'EN-FR', 'FR-EN']
                    }
                },
                'classification': {
                    'success': True,
                    'message': 'Classification service loaded successfully',
                    'data': {
                        'total_classifications': 3456,
                        'accuracy_rate': 89.5,
                        'categories': ['Support', 'Sales', 'Technical', 'General'],
                        'confidence_threshold': 0.85
                    }
                },
                
                # Users & Roles
                'users_roles': {
                    'success': True,
                    'message': 'Users & Roles loaded successfully',
                    'data': {
                        'total_users': 45,
                        'active_users': 38,
                        'total_roles': 8,
                        'recent_activity': [
                            {'user': 'john.doe', 'action': 'login', 'time': '2 minutes ago'},
                            {'user': 'jane.smith', 'action': 'role_update', 'time': '5 minutes ago'},
                            {'user': 'admin', 'action': 'user_create', 'time': '10 minutes ago'}
                        ]
                    }
                },
                'user_management': {
                    'success': True,
                    'message': 'User Management loaded successfully',
                    'data': {
                        'users': [
                            {'username': 'john.doe', 'role': 'Agent', 'status': 'Active'},
                            {'username': 'jane.smith', 'role': 'Supervisor', 'status': 'Active'},
                            {'username': 'admin', 'role': 'Administrator', 'status': 'Active'}
                        ],
                        'roles': ['Agent', 'Supervisor', 'Manager', 'Administrator']
                    }
                },
                'role_management': {
                    'success': True,
                    'message': 'Role Management loaded successfully',
                    'data': {
                        'roles': [
                            {'name': 'Agent', 'permissions': ['view_calls', 'create_cases']},
                            {'name': 'Supervisor', 'permissions': ['view_calls', 'manage_cases', 'view_reports']},
                            {'name': 'Administrator', 'permissions': ['all']}
                        ]
                    }
                },
                
                # Contacts
                'contacts': {
                    'success': True,
                    'message': 'Contacts loaded successfully',
                    'data': {
                        'total_contacts': 1250,
                        'active_contacts': 1189,
                        'recent_contacts': 23,
                        'contact_types': {'Client': 890, 'Partner': 234, 'Vendor': 126},
                        'recent_activity': [
                            {'contact': 'John Smith', 'action': 'updated', 'time': '1 hour ago'},
                            {'contact': 'Jane Doe', 'action': 'created', 'time': '2 hours ago'},
                            {'contact': 'Bob Wilson', 'action': 'contacted', 'time': '3 hours ago'}
                        ]
                    }
                },
                'contact_management': {
                    'success': True,
                    'message': 'Contact Management loaded successfully',
                    'data': {
                        'contacts': [
                            {'name': 'John Smith', 'email': 'john@example.com', 'phone': '+1234567890'},
                            {'name': 'Jane Doe', 'email': 'jane@example.com', 'phone': '+1234567891'},
                            {'name': 'Bob Wilson', 'email': 'bob@example.com', 'phone': '+1234567892'}
                        ],
                        'categories': ['Client', 'Partner', 'Vendor', 'Internal']
                    }
                },
                'contact_analytics': {
                    'success': True,
                    'message': 'Contact Analytics loaded successfully',
                    'data': {
                        'contact_growth': [45, 52, 38, 61, 78, 89, 95],
                        'interaction_frequency': [2.3, 1.8, 3.1, 2.7, 2.1, 2.9, 2.4],
                        'top_contacts': ['John Smith', 'Jane Doe', 'Bob Wilson']
                    }
                },
                
                # System Services
                'system_services': {
                    'success': True,
                    'message': 'System Services loaded successfully',
                    'data': {
                        'services': [
                            {'name': 'Database', 'status': 'healthy', 'uptime': '99.9%'},
                            {'name': 'API Gateway', 'status': 'healthy', 'uptime': '99.8%'},
                            {'name': 'File Storage', 'status': 'healthy', 'uptime': '99.7%'}
                        ],
                        'system_health': 'Excellent',
                        'last_backup': '2024-01-01 02:00:00'
                    }
                },
                'system_monitoring': {
                    'success': True,
                    'message': 'System Monitoring loaded successfully',
                    'data': {
                        'cpu_usage': 45.2,
                        'memory_usage': 67.8,
                        'disk_usage': 34.5,
                        'network_traffic': 125.6,
                        'alerts': ['Low disk space warning', 'High memory usage']
                    }
                },
                
                # Documentation
                'documentation': {
                    'success': True,
                    'message': 'Documentation loaded successfully',
                    'data': {
                        'total_documents': 156,
                        'active_contributors': 18,
                        'total_views': 2847,
                        'average_rating': 4.8,
                        'categories': [
                            {'name': 'System Documentation', 'count': 24, 'status': 'new'},
                            {'name': 'User Guides', 'count': 18, 'status': 'updated'},
                            {'name': 'API Reference', 'count': 32, 'status': 'popular'},
                            {'name': 'Reports & Analytics', 'count': 15, 'status': 'updated'},
                            {'name': 'Troubleshooting', 'count': 28, 'status': 'popular'},
                            {'name': 'Tutorials', 'count': 12, 'status': 'new'}
                        ],
                        'recent_documents': [
                            {'title': 'Getting Started with Call Management', 'category': 'User Guide', 'updated': '2 hours ago'},
                            {'title': 'API Authentication Guide', 'category': 'API Reference', 'updated': '4 hours ago'},
                            {'title': 'Advanced Analytics Dashboard', 'category': 'Reports & Analytics', 'updated': '6 hours ago'},
                            {'title': 'Troubleshooting Common Issues', 'category': 'Troubleshooting', 'updated': '1 day ago'}
                        ],
                        'popular_documents': [
                            {'title': 'Quick Start Guide', 'views': 1247, 'rating': 4.9},
                            {'title': 'API Integration Tutorial', 'views': 892, 'rating': 4.8},
                            {'title': 'User Management Guide', 'views': 756, 'rating': 4.7},
                            {'title': 'Reporting Best Practices', 'views': 634, 'rating': 4.6},
                            {'title': 'System Configuration', 'views': 521, 'rating': 4.5}
                        ]
                    }
                },
                'user_guide': {
                    'success': True,
                    'message': 'User Guide loaded successfully',
                    'data': {
                        'sections': ['Introduction', 'Getting Started', 'Features', 'Troubleshooting'],
                        'last_updated': '2024-01-01',
                        'version': '2.0.1'
                    }
                },
                
                # Chatbot
                'chatbot': {
                    'success': True,
                    'message': 'Chatbot data loaded successfully',
                    'data': {
                        'total_conversations': 2847,
                        'active_sessions': 23,
                        'avg_response_time': '0.8s',
                        'success_rate': '94.2%',
                        'recent_conversations': [
                            {
                                'id': 'conv-001',
                                'user': 'John Doe',
                                'time': '2 min ago',
                                'preview': 'I need help with my account settings...',
                                'intent': 'General Query',
                                'status': 'active'
                            },
                            {
                                'id': 'conv-002',
                                'user': 'Jane Smith',
                                'time': '5 min ago',
                                'preview': 'How do I reset my password?',
                                'intent': 'Support',
                                'status': 'completed'
                            },
                            {
                                'id': 'conv-003',
                                'user': 'Bob Wilson',
                                'time': '8 min ago',
                                'preview': 'I have an urgent billing issue...',
                                'intent': 'Emergency',
                                'status': 'escalated'
                            }
                        ],
                        'satisfaction': {
                            'positive': 89,
                            'positive_count': 1234,
                            'neutral': 8,
                            'neutral_count': 111,
                            'negative': 3,
                            'negative_count': 42
                        },
                        'training': {
                            'total_intents': 24,
                            'training_phrases': 1847,
                            'response_templates': 156,
                            'model_accuracy': 94.2,
                            'training_coverage': 87.5,
                            'fallback_rate': 5.8
                        },
                        'recent_activity': [
                            {
                                'icon': '🤖',
                                'title': 'New Intent Added',
                                'description': '"Billing Inquiry" intent created with 15 training phrases',
                                'time': '2 hours ago'
                            },
                            {
                                'icon': '📊',
                                'title': 'Model Retrained',
                                'description': 'Chatbot model updated with new training data',
                                'time': '4 hours ago'
                            },
                            {
                                'icon': '⚠️',
                                'title': 'High Fallback Rate',
                                'description': 'Fallback rate increased to 6.2% in last hour',
                                'time': '6 hours ago'
                            },
                            {
                                'icon': '✅',
                                'title': 'Performance Improved',
                                'description': 'Response time reduced by 15% after optimization',
                                'time': '1 day ago'
                            }
                        ],
                        'conversations_table': [
                            {
                                'id': 'conv-001',
                                'user': 'John Doe',
                                'intent': 'General Query',
                                'status': 'active',
                                'duration': '2:34',
                                'messages': 8,
                                'satisfaction': 4.5,
                                'created': '2 min ago'
                            },
                            {
                                'id': 'conv-002',
                                'user': 'Jane Smith',
                                'intent': 'Support',
                                'status': 'completed',
                                'duration': '4:12',
                                'messages': 12,
                                'satisfaction': 5.0,
                                'created': '5 min ago'
                            },
                            {
                                'id': 'conv-003',
                                'user': 'Bob Wilson',
                                'intent': 'Emergency',
                                'status': 'escalated',
                                'duration': '6:45',
                                'messages': 15,
                                'satisfaction': 2.0,
                                'created': '8 min ago'
                            }
                        ]
                    }
                },
                
                # Dashboard
                'dashboard': {
                    'success': True,
                    'message': 'Dashboard loaded successfully',
                    'data': {
                        'overview': {
                            'total_calls': 1250,
                            'total_cases': 890,
                            'active_users': 38,
                            'system_health': 'Excellent'
                        },
                        'quick_stats': {
                            'calls_today': 45,
                            'cases_resolved': 23,
                            'new_contacts': 12,
                            'ai_requests': 156
                        }
                    }
                }
            }
            
            # Return the appropriate mock data
            if filename in mock_data:
                return jsonify(mock_data[filename])
            else:
                # Default response for unknown filenames
                return jsonify({
                    'success': True,
                    'message': f'Data for {filename} loaded successfully',
                    'data': {
                        'filename': filename,
                        'timestamp': '2024-01-01T00:00:00Z',
                        'status': 'active'
                    }
                })

        except Exception as e:
            data['error'] = f"Error in Unified Data Route: {e}"
            logger.critical(data['error'])
            return jsonify(data), 404

    # Call Center Routes
    @app.route("/calls/form", methods=['GET'])
    def calls_form():
        logger.info("Call Center Form Page")
        return render_template('forms/form_calls.html', title="Call Center Form")

    @app.route("/calls/table", methods=['GET'])
    def calls_table():
        logger.info("Call Center Table Page")
        return render_template('tables/table_calls.html', title="Call Center Table")

    # Cases Routes
    @app.route("/cases/form", methods=['GET'])
    def cases_form():
        logger.info("Cases Form Page")
        return render_template('forms/form_cases.html', title="Cases Form")

    @app.route("/cases/table", methods=['GET'])
    def cases_table():
        logger.info("Cases Table Page")
        return render_template('tables/table_cases.html', title="Cases Table")

    # Users Routes
    @app.route("/users/form", methods=['GET'])
    def users_form():
        logger.info("Users Form Page")
        return render_template('forms/form_users.html', title="Users Form")

    @app.route("/users/table", methods=['GET'])
    def users_table():
        logger.info("Users Table Page")
        return render_template('tables/table_users.html', title="Users Table")

    # Clients Routes (using Users templates)
    @app.route("/clients/form", methods=['GET'])
    def clients_form():
        logger.info("Clients Form Page")
        return render_template('forms/form_users.html', title="Clients Form") # Uses users form template

    @app.route("/clients/table", methods=['GET'])
    def clients_table():
        logger.info("Clients Table Page")
        return render_template('tables/table_users.html', title="Clients Table") # Uses users table template

    # Handle View Errors
    @app.errorhandler(403)
    def forbidden(error):
        logger.warn("Helpline Error 403 " + str(request.headers.get('X-Real-IP')))

        data = {}
        data['code'] = 403
        data['method'] = request.method
        data['remote'] = request.remote_addr
        data['realip'] = request.headers.get('X-Real-IP')
        data['forward'] = request.headers.get('X-Forwarded-For')

        # system.indexcreate(data)

        if request.method == "POST":
            return jsonify({}), 403

        return render_template('errors/403.html')

    @app.errorhandler(404)
    def page_not_found(error):
        logger.warn("Helpline Error 404 " + str(request.headers.get('X-Real-IP')))

        data = {}
        data['code'] = 404
        data['method'] = request.method
        data['remote'] = request.remote_addr
        data['realip'] = request.headers.get('X-Real-IP')
        data['forward'] = request.headers.get('X-Forwarded-For')

        # system.indexcreate(data)

        if request.method == "POST":
            return jsonify({}), 404

        return render_template('errors/404.html')

    @app.errorhandler(405)
    def method_not_allowed(error):
        logger.warn("Helpline Error 405 " + str(request.headers.get('X-Real-IP')))

        data = {}
        data['code'] = 405
        data['method'] = request.method
        data['remote'] = request.remote_addr
        data['realip'] = request.headers.get('X-Real-IP')
        data['forward'] = request.headers.get('X-Forwarded-For')

        # system.indexcreate(data)

        if request.method == "POST":
            return jsonify({}), 405

        return render_template('errors/405.html')

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.warn("Helpline Error 500 " + str(request.headers.get('X-Real-IP')))

        data = {}
        data['code'] = 405
        data['method'] = request.method
        data['remote'] = request.remote_addr
        data['realip'] = request.headers.get('X-Real-IP')
        data['forward'] = request.headers.get('X-Forwarded-For')

        # system.indexcreate(data)

        if request.method == "POST":
            return jsonify({}), 500

        return render_template('errors/500.html')

    return app
