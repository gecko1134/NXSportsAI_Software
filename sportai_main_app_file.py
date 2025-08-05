import os
import sys
import streamlit as st
import json
from typing import Dict, Any

# Add current directory to Python path
BASE_DIR = os.path.dirname(__file__)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Import AI modules (with error handling)
try:
    from ai_modules.demand_forecasting import DemandForecaster
    from ai_modules.scheduling_optimizer import optimize_schedule
    from ai_modules.sponsorship_matcher import match_sponsors
    from ai_modules.dynamic_contract_generator import generate_contract
    from ai_modules.membership_churn import ChurnPredictor
    from ai_modules.marketing_optimizer import optimize_campaign
    AI_MODULES_AVAILABLE = True
except ImportError as e:
    AI_MODULES_AVAILABLE = False

# Import all other modules with error handling
def safe_import(module_name):
    """Safely import a module and return it, or None if import fails"""
    try:
        return __import__(module_name)
    except ImportError:
        return None

# Core modules mapping
modules = {
    'auth': safe_import('auth'),
    'header_loader': safe_import('header_loader'),
    
    # AI Tools
    'ai_event_forecast': safe_import('ai_event_forecast'),
    'ai_matchmaker_tool': safe_import('ai_matchmaker_tool'),
    'ai_revenue_maximizer': safe_import('ai_revenue_maximizer'),
    'ai_scheduler_tool': safe_import('ai_scheduler_tool'),
    'ai_scheduling_suggestions': safe_import('ai_scheduling_suggestions'),
    'ai_sponsor_opportunity_finder': safe_import('ai_sponsor_opportunity_finder'),
    'ai_strategy_dashboard': safe_import('ai_strategy_dashboard'),
    'ai_suggestion_digest': safe_import('ai_suggestion_digest'),
    'ai_voice_command': safe_import('ai_voice_command'),
    'ai_facility_chat': safe_import('ai_facility_chat'),
    'ai_voice_responder': safe_import('ai_voice_responder'),
    
    # Core Management
    'central_dashboard': safe_import('central_dashboard'),
    'event_control_panel': safe_import('event_control_panel'),
    'event_creator_ai': safe_import('event_creator_ai'),
    'facility_master_tracker': safe_import('facility_master_tracker'),
    'membership_dashboard': safe_import('membership_dashboard'),
    
    # Facility Management
    'facility_access_tracker': safe_import('facility_access_tracker'),
    'facility_capacity_alerts': safe_import('facility_capacity_alerts'),
    'facility_contract_monitor': safe_import('facility_contract_monitor'),
    'facility_layout_map': safe_import('facility_layout_map'),
    'facility_membership_monitor': safe_import('facility_membership_monitor'),
    'complex_usage_optimizer': safe_import('complex_usage_optimizer'),
    'dome_usage_tool': safe_import('dome_usage_tool'),
    'surface_usage_by_type': safe_import('surface_usage_by_type'),
    'surface_demand_heatmap': safe_import('surface_demand_heatmap'),
    'adaptive_use_planner': safe_import('adaptive_use_planner'),
    
    # Membership & CRM
    'membership_credit_tracker': safe_import('membership_credit_tracker'),
    'membership_crm_tracker': safe_import('membership_crm_tracker'),
    'membership_goal_tracker': safe_import('membership_goal_tracker'),
    'membership_insights_ai': safe_import('membership_insights_ai'),
    'membership_loyalty_rewards': safe_import('membership_loyalty_rewards'),
    'membership_marketing_ai': safe_import('membership_marketing_ai'),
    'member_portal': safe_import('member_portal'),
    'member_selector': safe_import('member_selector'),
    
    # Sponsorship & Revenue
    'sponsor_dashboard': safe_import('sponsor_dashboard'),
    'sponsorship_ai_calculator': safe_import('sponsorship_ai_calculator'),
    'sponsorship_availability': safe_import('sponsorship_availability'),
    'sponsorship_contract_generator': safe_import('sponsorship_contract_generator'),
    'sponsorship_inventory_manager': safe_import('sponsorship_inventory_manager'),
    'sponsorship_roi_tracker': safe_import('sponsorship_roi_tracker'),
    'sponsorship_tracker': safe_import('sponsorship_tracker'),
    'sponsor_portal': safe_import('sponsor_portal'),
    'revenue_heatmap': safe_import('revenue_heatmap'),
    'revenue_projection_simulator': safe_import('revenue_projection_simulator'),
    'sponsorship_revenue_builder': safe_import('sponsorship_revenue_builder'),
    'ai_sponsor_pricing_trends': safe_import('ai_sponsor_pricing_trends'),
    'sponsor_pitch_portal': safe_import('sponsor_pitch_portal'),
    'sponsor_pitchbook_builder': safe_import('sponsor_pitchbook_builder'),
    'sponsor_pdf_packet': safe_import('sponsor_pdf_packet'),
    'sponsor_link_sender': safe_import('sponsor_link_sender'),
    'sponsor_map_viewer': safe_import('sponsor_map_viewer'),
    
    # Events & Sports
    'tournament_scheduler': safe_import('tournament_scheduler'),
    'esports_manager': safe_import('esports_manager'),
    'adaptive_sports_center': safe_import('adaptive_sports_center'),
    'league_coordinator': safe_import('league_coordinator'),
    'team_club_manager': safe_import('team_club_manager'),
    'sport_library': safe_import('sport_library'),
    'event_profit_analyzer': safe_import('event_profit_analyzer'),
    'event_admin': safe_import('event_admin'),
    'international_team_portal': safe_import('international_team_portal'),
    'park_activity_dashboard': safe_import('park_activity_dashboard'),
    
    # Financial & Reporting
    'board_pdf_exporter': safe_import('board_pdf_exporter'),
    'finance_feed_connector': safe_import('finance_feed_connector'),
    'financial_feed_sync': safe_import('financial_feed_sync'),
    'revenue_proforma_auto': safe_import('revenue_proforma_auto'),
    'weekly_report_generator': safe_import('weekly_report_generator'),
    'report_download_portal': safe_import('report_download_portal'),
    'board_packet_pdf_generator': safe_import('board_packet_pdf_generator'),
    'board_report_scheduler': safe_import('board_report_scheduler'),
    'pdf_export_tool': safe_import('pdf_export_tool'),
    
    # Grants & Fundraising
    'grant_renewal_manager': safe_import('grant_renewal_manager'),
    'grant_alert_center': safe_import('grant_alert_center'),
    'grant_writer_ai': safe_import('grant_writer_ai'),
    'grant_match_ai': safe_import('grant_match_ai'),
    'grant_status_manager': safe_import('grant_status_manager'),
    'pdf_grant_exporter': safe_import('pdf_grant_exporter'),
    'investor_kit_generator': safe_import('investor_kit_generator'),
    'investor_pitch_portal': safe_import('investor_pitch_portal'),
    'funding_narrative_sync': safe_import('funding_narrative_sync'),
    
    # Donations
    'donation_landing_page': safe_import('donation_landing_page'),
    'donation_checkout': safe_import('donation_checkout'),
    'donation_campaign_viewer': safe_import('donation_campaign_viewer'),
    'donation_goal_tracker': safe_import('donation_goal_tracker'),
    'donor_profile_creator': safe_import('donor_profile_creator'),
    'crm_export_generator': safe_import('crm_export_generator'),
    'crm_grant_donor_sync': safe_import('crm_grant_donor_sync'),
    
    # Communications & Alerts
    'email_notifications': safe_import('email_notifications'),
    'sms_alert_center': safe_import('sms_alert_center'),
    'slack_alert_center': safe_import('slack_alert_center'),
    'member_alerts_auto': safe_import('member_alerts_auto'),
    'usage_alerts_auto': safe_import('usage_alerts_auto'),
    'contract_alerts_auto': safe_import('contract_alerts_auto'),
    'credential_expiry_alerts': safe_import('credential_expiry_alerts'),
    'daily_task_scheduler': safe_import('daily_task_scheduler'),
    
    # Integrations & Tools
    'google_sheets_sync': safe_import('google_sheets_sync'),
    'gsheets_sync': safe_import('gsheets_sync'),
    'webhook_automation': safe_import('webhook_automation'),
    'pandadoc_contract': safe_import('pandadoc_contract'),
    'auto_contract_generator': safe_import('auto_contract_generator'),
    'hubspot_deal_logger': safe_import('hubspot_deal_logger'),
    'mailchimp_lead_collector': safe_import('mailchimp_lead_collector'),
    
    # Marketing & Media
    'marketing_flipbook_generator': safe_import('marketing_flipbook_generator'),
    'marketing_packet_builder': safe_import('marketing_packet_builder'),
    'flipbook_embedder': safe_import('flipbook_embedder'),
    'flipbook_pitch_creator': safe_import('flipbook_pitch_creator'),
    'screen_rotation_scheduler': safe_import('screen_rotation_scheduler'),
    'media_display_rotator': safe_import('media_display_rotator'),
    
    # Governance & Admin
    'governance_admin': safe_import('governance_admin'),
    'governance_diagram': safe_import('governance_diagram'),
    'governance_tool': safe_import('governance_tool'),
    'admin_override_console': safe_import('admin_override_console'),
    'admin_sidebar_badges': safe_import('admin_sidebar_badges'),
    'platform_guidebook_writer': safe_import('platform_guidebook_writer'),
    
    # Utilities
    'dynamic_pricing_tool': safe_import('dynamic_pricing_tool'),
    'visual_calendar_layout': safe_import('visual_calendar_layout'),
    'mobile_friendly_ui': safe_import('mobile_friendly_ui'),
    'real_time_dashboard': safe_import('real_time_dashboard'),
    'setup_assistant_ai': safe_import('setup_assistant_ai'),
    'portal_router': safe_import('portal_router'),
    'upsell_offer_engine': safe_import('upsell_offer_engine'),
    'public_schedule': safe_import('public_schedule'),
    'expiring_link_manager': safe_import('expiring_link_manager'),
    
    # Specialty Programs
    'scholarship_fund_manager': safe_import('scholarship_fund_manager'),
    'scholarship_tracker': safe_import('scholarship_tracker'),
    'mentorship_center': safe_import('mentorship_center'),
    'volunteer_hub': safe_import('volunteer_hub'),
    'student_committee': safe_import('student_committee'),
    'referee_manager': safe_import('referee_manager'),
    'nil_tracker': safe_import('nil_tracker'),
    'trail_access_planner': safe_import('trail_access_planner'),
    
    # Contract & Performance
    'contract_insights_ai': safe_import('contract_insights_ai'),
    'contract_usage_tracker': safe_import('contract_usage_tracker'),
    'performance_goal_ai': safe_import('performance_goal_ai'),
    'facility_membership_comparator_ai': safe_import('facility_membership_comparator_ai'),
    'membership_ticketing_integration': safe_import('membership_ticketing_integration'),
    'sponsorship_inventory_limiter': safe_import('sponsorship_inventory_limiter'),
}

# Filter out None values (failed imports)
available_modules = {k: v for k, v in modules.items() if v is not None}

class SportAIApp:
    def __init__(self):
        self.users = self.load_users()
        self.tools = self.build_tools_menu()

    def load_users(self) -> Dict[str, Any]:
        """Load user data securely and create default users if needed."""
        file_path = 'users.json'
        default_users = {
            "admin@sportai.com": {"password": hash_pw("admin123"), "role": "admin"},
            "manager@sportai.com": {"password": hash_pw("manager123"), "role": "manager"},
            "user@sportai.com": {"password": hash_pw("user123"), "role": "user"},
        }
        try:
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    json.dump(default_users, f, indent=2)
                return default_users
            else:
                with open(file_path, "r") as f:
                    users = json.load(f)
                # If old (plaintext) users.json, upgrade
                updated = False
                for k, v in users.items():
                    if len(v['password']) != 64:  # not hex sha256
                        v['password'] = hash_pw(v['password'])
                        updated = True
                if updated:
                    with open(file_path, "w") as f:
                        json.dump(users, f, indent=2)
                return users
        except Exception as e:
            st.error(f"User loading failed: {e}")
            logging.error(f"load_users error: {e}")
            return default_users

    def build_tools_menu(self) -> Dict[str, Any]:
        """Only show tools whose modules loaded successfully."""
        # (Reuse your tool_categories dict as before)
        tool_categories = {
            # ... (omitted for brevity, same as your original)
        }
        tools = {}
        for tool_name, module_key in tool_categories.items():
            if module_key in available_modules:
                tools[tool_name] = available_modules[module_key]
        return tools

    def login(self):
        st.sidebar.header('🔐 Login')
        email = st.sidebar.text_input('Email', key='login_email')
        password = st.sidebar.text_input('Password', type='password', key='login_password')
        if st.sidebar.button('Login'):
            user = self.users.get(email)
            if user and verify_pw(password, user['password']):
                st.session_state.user = {'email': email, 'role': user['role']}
                st.sidebar.success('✅ Login successful!')
                st.rerun()
            else:
                st.sidebar.error('❌ Invalid credentials.')
        with st.sidebar.expander("📝 Demo Accounts"):
            st.write("**Admin:** admin@sportai.com / admin123")
            st.write("**Manager:** manager@sportai.com / manager123")
            st.write("**User:** user@sportai.com / user123")

    def logout(self):
        if st.sidebar.button('🚪 Logout'):
            st.session_state.user = None
            st.rerun()
            }
            try:
                with open('users.json', 'w') as f:
                    json.dump(default_users, f, indent=2)
                return default_users
            except Exception:
                return default_users
        except Exception as e:
            st.error(f"Error loading users: {e}")
            return {}
    
    def build_tools_menu(self) -> Dict[str, Any]:
        """Build the tools menu from available modules, organized by categories"""
        tools = {}
        
        # Define tool categories with their corresponding modules
        tool_categories = {
            # AI Tools
            "🤖 AI Event Forecast": 'ai_event_forecast',
            "🤖 AI Matchmaker": 'ai_matchmaker_tool',
            "🤖 AI Revenue Maximizer": 'ai_revenue_maximizer',
            "🤖 AI Scheduler": 'ai_scheduler_tool',
            "🤖 AI Scheduling Suggestions": 'ai_scheduling_suggestions',
            "🤖 AI Sponsor Finder": 'ai_sponsor_opportunity_finder',
            "🤖 AI Strategy Dashboard": 'ai_strategy_dashboard',
            "🤖 AI Suggestion Digest": 'ai_suggestion_digest',
            "🤖 AI Voice Command": 'ai_voice_command',
            "🤖 AI Facility Chat": 'ai_facility_chat',
            "🤖 AI Voice Assistant": 'ai_voice_responder',
            "🤖 AI Sponsor Pricing": 'ai_sponsor_pricing_trends',
            "🤖 AI Grant Writer": 'grant_writer_ai',
            "🤖 AI Grant Match": 'grant_match_ai',
            
            # Core Management
            "📊 Central Dashboard": 'central_dashboard',
            "🎯 Event Control Panel": 'event_control_panel',
            "🎨 Event Creator AI": 'event_creator_ai',
            "🏟️ Facility Master Tracker": 'facility_master_tracker',
            "👥 Membership Dashboard": 'membership_dashboard',
            "💰 Sponsor Dashboard": 'sponsor_dashboard',
            "⚡ Real-Time Dashboard": 'real_time_dashboard',
            "🛠️ Setup Assistant AI": 'setup_assistant_ai',
            
            # Facility Management
            "🚪 Facility Access Tracker": 'facility_access_tracker',
            "⚠️ Facility Capacity Alerts": 'facility_capacity_alerts',
            "📋 Facility Contract Monitor": 'facility_contract_monitor',
            "🗺️ Facility Layout Map": 'facility_layout_map',
            "👥 Facility Membership Monitor": 'facility_membership_monitor',
            "🔧 Complex Usage Optimizer": 'complex_usage_optimizer',
            "🏛️ Dome Usage Tool": 'dome_usage_tool',
            "📊 Surface Usage by Type": 'surface_usage_by_type',
            "🔥 Surface Demand Heatmap": 'surface_demand_heatmap',
            "📈 Adaptive Use Planner": 'adaptive_use_planner',
            
            # Membership & CRM
            "💳 Membership Credit Tracker": 'membership_credit_tracker',
            "👥 Membership CRM Tracker": 'membership_crm_tracker',
            "🎯 Membership Goal Tracker": 'membership_goal_tracker',
            "📊 Membership Insights AI": 'membership_insights_ai',
            "🏆 Membership Loyalty Rewards": 'membership_loyalty_rewards',
            "📢 Membership Marketing AI": 'membership_marketing_ai',
            "🔗 Membership Ticketing Integration": 'membership_ticketing_integration',
            "🚪 Member Portal": 'member_portal',
            "🎯 Member Selector": 'member_selector',
            
            # Sponsorship & Revenue
            "🤝 Sponsorship AI Calculator": 'sponsorship_ai_calculator',
            "📅 Sponsorship Availability": 'sponsorship_availability',
            "📄 Sponsorship Contract Generator": 'sponsorship_contract_generator',
            "📦 Sponsorship Inventory Manager": 'sponsorship_inventory_manager',
            "📈 Sponsorship ROI Tracker": 'sponsorship_roi_tracker',
            "📊 Sponsorship Tracker": 'sponsorship_tracker',
            "🚪 Sponsor Portal": 'sponsor_portal',
            "💰 Sponsorship Revenue Builder": 'sponsorship_revenue_builder',
            "🎯 Sponsor Pitch Portal": 'sponsor_pitch_portal',
            "📖 Sponsor Pitchbook Builder": 'sponsor_pitchbook_builder',
            "📄 Sponsor PDF Packet": 'sponsor_pdf_packet',
            "🔗 Sponsor Link Sender": 'sponsor_link_sender',
            "🗺️ Sponsor Map Viewer": 'sponsor_map_viewer',
            
            # Financial Tools
            "🔥 Revenue Heatmap": 'revenue_heatmap',
            "📈 Revenue Projection Simulator": 'revenue_projection_simulator',
            "📊 Revenue Proforma Auto": 'revenue_proforma_auto',
            "💰 Dynamic Pricing Tool": 'dynamic_pricing_tool',
            "💼 Finance Feed Connector": 'finance_feed_connector',
            "🔄 Financial Feed Sync": 'financial_feed_sync',
            
            # Sports & Events
            "🏆 Tournament Scheduler": 'tournament_scheduler',
            "🎮 Esports Manager": 'esports_manager',
            "♿ Adaptive Sports Center": 'adaptive_sports_center',
            "🏟️ League Coordinator": 'league_coordinator',
            "👥 Team Club Manager": 'team_club_manager',
            "📚 Sport Library": 'sport_library',
            "💰 Event Profit Analyzer": 'event_profit_analyzer',
            "🎯 Event Admin": 'event_admin',
            "🌍 International Team Portal": 'international_team_portal',
            "🏞️ Park Activity Dashboard": 'park_activity_dashboard',
            
            # Reporting & Documents
            "📋 Board PDF Exporter": 'board_pdf_exporter',
            "📊 Board Packet Generator": 'board_packet_pdf_generator',
            "📅 Board Report Scheduler": 'board_report_scheduler',
            "📄 Weekly Report Generator": 'weekly_report_generator',
            "📥 Report Download Portal": 'report_download_portal',
            "📄 PDF Export Tool": 'pdf_export_tool',
            
            # Communications
            "📧 Email Notifications": 'email_notifications',
            "📱 SMS Alert Center": 'sms_alert_center',
            "💬 Slack Alert Center": 'slack_alert_center',
            "⚠️ Member Alerts Auto": 'member_alerts_auto',
            "📊 Usage Alerts Auto": 'usage_alerts_auto',
            "📋 Contract Alerts Auto": 'contract_alerts_auto',
            "🔐 Credential Expiry Alerts": 'credential_expiry_alerts',
            "📅 Daily Task Scheduler": 'daily_task_scheduler',
            
            # Marketing & Media
            "📦 Marketing Packet Builder": 'marketing_packet_builder',
            "📖 Marketing Flipbook Generator": 'marketing_flipbook_generator',
            "📚 Flipbook Embedder": 'flipbook_embedder',
            "🎨 Flipbook Pitch Creator": 'flipbook_pitch_creator',
            "🔄 Screen Rotation Scheduler": 'screen_rotation_scheduler',
            "📺 Media Display Rotator": 'media_display_rotator',
            
            # Integrations
            "📊 Google Sheets Sync": 'google_sheets_sync',
            "🔄 GSheets Sync": 'gsheets_sync',
            "🔗 Webhook Automation": 'webhook_automation',
            "📄 PandaDoc Contract": 'pandadoc_contract',
            "🤖 Auto Contract Generator": 'auto_contract_generator',
            "🔄 HubSpot Deal Logger": 'hubspot_deal_logger',
            "📧 Mailchimp Lead Collector": 'mailchimp_lead_collector',
            
            # Utilities
            "📱 Mobile Friendly UI": 'mobile_friendly_ui',
            "📅 Visual Calendar Layout": 'visual_calendar_layout',
            "🔧 Admin Override Console": 'admin_override_console',
            "🏷️ Admin Sidebar Badges": 'admin_sidebar_badges',
            "📚 Platform Guidebook": 'platform_guidebook_writer',
            "🔗 Portal Router": 'portal_router',
            "💎 Upsell Offer Engine": 'upsell_offer_engine',
            "📅 Public Schedule": 'public_schedule',
            "⏰ Expiring Link Manager": 'expiring_link_manager',
        }
        
        # Add tools that have available modules
        for tool_name, module_key in tool_categories.items():
            if module_key in available_modules:
                tools[tool_name] = available_modules[module_key]
        
        return tools
    
    def login(self):
        """Handle user login interface"""
        st.sidebar.header('🔐 Login')
        email = st.sidebar.text_input('Email', key='login_email')
        password = st.sidebar.text_input('Password', type='password', key='login_password')
        
        if st.sidebar.button('Login'):
            user = self.users.get(email)
            if user and user['password'] == password:
                st.session_state.user = {'email': email, 'role': user['role']}
                st.sidebar.success('✅ Login successful!')
                st.rerun()
            else:
                st.sidebar.error('❌ Invalid credentials.')
        
        # Show available demo accounts
        with st.sidebar.expander("📝 Demo Accounts"):
            st.write("**Admin:** admin@sportai.com / admin123")
            st.write("**Manager:** manager@sportai.com / manager123")
            st.write("**User:** user@sportai.com / user123")
    
    def logout(self):
        """Handle user logout"""
        if st.sidebar.button('🚪 Logout'):
            st.session_state.user = None
            st.rerun()
    
    def render_ai_sidebar(self):
        """Render the AI optimization sidebar with core AI functions"""
        if not AI_MODULES_AVAILABLE:
            st.sidebar.warning("⚠️ AI modules not available")
            return
            
        st.sidebar.markdown("---")
        st.sidebar.title('🤖 AI Optimizations')
        
        if st.sidebar.button('📈 Forecast Demand'):
            try:
                forecaster = DemandForecaster()
                st.success("✅ Demand forecasting initiated!")
                st.info("💡 Next: Load booking_data.csv and call DemandForecaster.predict()")
            except Exception as e:
                st.error(f"❌ Error in demand forecasting: {e}")
        
        if st.sidebar.button('📅 Optimize Schedule'):
            try:
                st.success("✅ Schedule optimization initiated!")
                st.info("💡 Next: Load schedule_requests.csv and resources.json")
            except Exception as e:
                st.error(f"❌ Error in schedule optimization: {e}")
        
        if st.sidebar.button('🤝 Match Sponsors'):
            try:
                st.success("✅ Sponsor matching initiated!")
                st.info("💡 Next: Load assets.csv and sponsors.csv")
            except Exception as e:
                st.error(f"❌ Error in sponsor matching: {e}")
        
        if st.sidebar.button('📄 Generate Contract'):
            try:
                st.success("✅ Dynamic contract generation initiated!")
                st.info("💡 Next: Call generate_contract(template_id, data, api_key)")
            except Exception as e:
                st.error(f"❌ Error in contract generation: {e}")
        
        if st.sidebar.button('⚠️ Predict Churn'):
            try:
                predictor = ChurnPredictor()
                st.success("✅ Churn prediction initiated!")
                st.info("💡 Next: Load member_features.csv")
            except Exception as e:
                st.error(f"❌ Error in churn prediction: {e}")
        
        if st.sidebar.button('📢 Optimize Campaign'):
            try:
                st.success("✅ Campaign optimization initiated!")
                st.info("💡 Next: Load invites.csv")
            except Exception as e:
                st.error(f"❌ Error in campaign optimization: {e}")
    
    def run(self):
        """Main application runner"""
        st.set_page_config(
            page_title='SportAI Suite - Venture North Admin',
            page_icon='🏟️',
            layout='wide',
            initial_sidebar_state='expanded'
        )
        
        # Check if user is logged in
        if 'user' not in st.session_state or not st.session_state.user:
            st.title('🏟️ SportAI Suite')
            st.markdown("""
            ### Welcome to the Comprehensive Sports Facility Management Platform
            
            SportAI Suite is your all-in-one solution for managing sports facilities, memberships, 
            sponsorships, events, and revenue optimization with cutting-edge AI technology.
            
            **Key Features:**
            - 🤖 AI-powered demand forecasting and scheduling optimization
            - 🏟️ Complete facility and membership management
            - 💰 Revenue optimization and sponsorship matching
            - 📊 Real-time analytics and reporting
            - 🎯 Event management and tournament scheduling
            - 📱 Mobile-friendly interface with multi-user support
            
            **Please log in using the sidebar to access all tools.**
            """)
            
            # Show quick stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Available Tools", len(self.tools))
            with col2:
                st.metric("AI Modules", "✅ Ready" if AI_MODULES_AVAILABLE else "❌ Not Available")
            with col3:
                st.metric("Loaded Modules", len(available_modules))
            
            self.login()
            return
        
        # User is logged in
        user = st.session_state.user
        st.sidebar.success(f"✅ Logged in as {user['email']} ({user['role'].title()})")
        self.logout()
        
        # Tool selection
        st.sidebar.markdown("---")
        st.sidebar.title('🧭 Select Tool')
        
        if not self.tools:
            st.sidebar.warning("⚠️ No tools available")
            st.title('🏟️ SportAI Suite')
            st.error('❌ No modules were successfully imported. Please check your installation.')
            st.markdown("""
            ### Troubleshooting Steps:
            1. Ensure all module files are in the correct directory
            2. Check that each module has a `run()` function
            3. Verify Python path configuration
            4. Review error logs for specific import issues
            """)
            return
        
        # Create searchable tool selection
        search_term = st.sidebar.text_input("🔍 Search Tools", placeholder="Type to filter tools...")
        
        # Filter tools based on search
        if search_term:
            filtered_tools = {k: v for k, v in self.tools.items() 
                            if search_term.lower() in k.lower()}
        else:
            filtered_tools = self.tools
        
        if not filtered_tools:
            st.sidebar.warning(f"No tools found matching '{search_term}'")
            filtered_tools = self.tools
        
        selection = st.sidebar.selectbox(
            'Choose a Tool',
            list(filtered_tools.keys()),
            key='tool_selection'
        )
        
        # Quick access buttons for popular tools
        st.sidebar.markdown("### 🚀 Quick Access")
        quick_tools = [
            "📊 Central Dashboard",
            "🤖 AI Strategy Dashboard", 
            "🏟️ Facility Master Tracker",
            "👥 Membership Dashboard",
            "💰 Sponsor Dashboard"
        ]
        
        for tool in quick_tools:
            if tool in self.tools:
                tool_display_name = tool.split(" ", 1)[1]  # Remove emoji for button
                if st.sidebar.button(tool_display_name, key=f"quick_{tool}"):
                    st.session_state.tool_selection = tool
                    st.rerun()
        
        # Render AI sidebar
        self.render_ai_sidebar()
        
        # Run selected tool
        if selection and selection in self.tools:
            tool_module = self.tools[selection]
            if tool_module and hasattr(tool_module, 'run'):
                try:
                    # Load header if available
                    if available_modules.get('header_loader'):
                        available_modules['header_loader'].run()
                    
                    # Show current tool info
                    st.info(f"🔧 Running: {selection}")
                    
                    # Run the selected tool
                    tool_module.run()
                    
                except Exception as e:
                    st.error(f"❌ Error running {selection}: {e}")
                    st.markdown("""
                    ### Troubleshooting:
                    - Check that the module is properly implemented
                    - Verify all required dependencies are installed
                    - Review the module's `run()` function for errors
                    """)
                    
                    # Show debug info for admins
                    if user['role'] == 'admin':
                        with st.expander("🔍 Debug Information"):
                            st.code(f"Module: {tool_module}")
                            st.code(f"Error: {str(e)}")
            else:
                st.error(f"❌ Tool '{selection}' is not properly configured.")
                st.write("The selected tool does not have a valid `run()` method.")
        else:
            # Main dashboard when no specific tool is selected
            st.title('🏟️ SportAI Suite with AI Modules')
            st.markdown(f"Welcome back, **{user['email']}**! Select a tool from the sidebar to get started.")
            
            # Show system status
            st.markdown("## 📊 System Status")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Available Tools", len(self.tools), delta=f"+{len(available_modules)} modules")
            
            with col2:
                status = "✅ Ready" if AI_MODULES_AVAILABLE else "❌ Not Available"
                st.metric("AI Modules", status)
            
            with col3:
                st.metric("User Role", user['role'].title())
            
            with col4:
                st.metric("Session Status", "🟢 Active")
            
            # Tool categories overview
            st.markdown("## 🛠️ Available Tool Categories")
            
            # Group tools by category based on emoji prefixes
            categories = {
                "🤖 AI Tools": [k for k in self.tools.keys() if k.startswith("🤖")],
                "📊 Management": [k for k in self.tools.keys() if k.startswith(("📊", "🎯", "🏟️", "👥", "💰", "⚡", "🛠️"))],
                "🏆 Sports & Events": [k for k in self.tools.keys() if k.startswith(("🏆", "🎮", "♿", "🌍", "🏞️"))],
                "💰 Financial": [k for k in self.tools.keys() if k.startswith(("🔥", "📈", "💼", "🔄"))],
                "📋 Reporting": [k for k in self.tools.keys() if k.startswith(("📋", "📄", "📅", "📥"))],
                "📢 Communications": [k for k in self.tools.keys() if k.startswith(("📧", "📱", "💬", "⚠️"))],
                "🔄 Integrations": [k for k in self.tools.keys() if k.startswith(("🔗", "🤖")) and not k.startswith("🤖 AI")],
                "🛠️ Utilities": [k for k in self.tools.keys() if k.startswith(("📱", "🔧", "🏷️", "📚", "💎", "⏰"))]
            }
            
            # Display categories in a grid
            category_cols = st.columns(2)
            for i, (category, tools) in enumerate(categories.items()):
                if tools:  # Only show categories with tools
                    with category_cols[i % 2]:
                        st.markdown(f"### {category}")
                        st.markdown(f"**{len(tools)} tools available**")
                        
                        # Show first 3 tools as examples
                        for tool in tools[:3]:
                            st.markdown(f"• {tool}")
                        
                        if len(tools) > 3:
                            st.markdown(f"• ... and {len(tools) - 3} more")
                        
                        st.markdown("---")
            
            # Quick actions section
            st.markdown("## 🚀 Quick Actions")
            
            action_cols = st.columns(3)
            
            with action_cols[0]:
                if st.button("📊 Open Central Dashboard", key="dashboard_btn", use_container_width=True):
                    if "📊 Central Dashboard" in self.tools:
                        st.session_state.tool_selection = "📊 Central Dashboard"
                        st.rerun()
            
            with action_cols[1]:
                if st.button("🤖 AI Strategy Dashboard", key="ai_dashboard_btn", use_container_width=True):
                    if "🤖 AI Strategy Dashboard" in self.tools:
                        st.session_state.tool_selection = "🤖 AI Strategy Dashboard"
                        st.rerun()
            
            with action_cols[2]:
                if st.button("🏟️ Facility Overview", key="facility_btn", use_container_width=True):
                    if "🏟️ Facility Master Tracker" in self.tools:
                        st.session_state.tool_selection = "🏟️ Facility Master Tracker"
                        st.rerun()
            
            # Show module import status for admins
            if user['role'] == 'admin':
                with st.expander("🔍 Module Import Status (Admin Only)"):
                    st.markdown("### Successfully Loaded Modules:")
                    for module_name in sorted(available_modules.keys()):
                        st.markdown(f"✅ {module_name}")
                    
                    st.markdown("### Failed Imports:")
                    failed_modules = [k for k, v in modules.items() if v is None]
                    if failed_modules:
                        for module_name in sorted(failed_modules):
                            st.markdown(f"❌ {module_name}")
                    else:
                        st.markdown("✅ All modules loaded successfully!")
                    
                    st.markdown(f"**Total Available:** {len(available_modules)}/{len(modules)} modules")
            
            # Show helpful tips
            st.markdown("## 💡 Tips & Getting Started")
            
            tips_cols = st.columns(2)
            
            with tips_cols[0]:
                st.markdown("### Navigation Tips")
                st.markdown("""
                • Use the **search box** in the sidebar to quickly find tools
                • **Quick Access** buttons provide shortcuts to popular tools
                • Tools are **color-coded** by category with emoji indicators
                • **Admin users** can see debug information when errors occur
                """)
            
            with tips_cols[1]:
                st.markdown("### AI Features")
                if AI_MODULES_AVAILABLE:
                    st.markdown("""
                    • **AI Optimization** buttons are in the sidebar
                    • Use **AI Strategy Dashboard** for comprehensive insights
                    • **Demand forecasting** helps optimize facility usage
                    • **Sponsor matching** AI finds the best partnerships
                    """)
                else:
                    st.markdown("""
                    • AI modules are **not currently available**
                    • Check your `ai_modules/` directory structure
                    • Ensure all AI dependencies are installed
                    • Contact support if issues persist
                    """)
            
            # Footer with version and support info
            st.markdown("---")
            st.markdown("""
            <div style='text-align: center; color: #666; padding: 20px;'>
                <p><strong>SportAI Suite v2.0</strong> | Venture North Admin Platform</p>
                <p>For support, contact your system administrator</p>
            </div>
            """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    app = SportAIApp()
    app.run()
