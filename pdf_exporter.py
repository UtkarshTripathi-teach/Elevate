from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime, timedelta
import pandas as pd
import io
from utils import format_time

class PDFExporter:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for the PDF"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2E86AB')
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.HexColor('#A23B72')
        )
        
        # Header style
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.HexColor('#F18F01')
        )
        
        # Normal text with custom color
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8
        )
        
        # Highlight style for important information
        self.highlight_style = ParagraphStyle(
            'Highlight',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#C73E1D'),
            spaceAfter=8
        )
    
    def generate_report(self, username, user_data, period, quiz_data=None):
        """Generate a comprehensive study report PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        story = []
        
        # Add title and header information
        story.extend(self._create_header(username, period))
        
        # Add executive summary
        story.extend(self._create_executive_summary(user_data, quiz_data))
        
        # Add detailed statistics
        story.extend(self._create_detailed_statistics(user_data, quiz_data))
        
        # Add subject breakdown
        story.extend(self._create_subject_breakdown(user_data))
        
        # Add performance analysis
        story.extend(self._create_performance_analysis(user_data))
        
        # Add recommendations
        story.extend(self._create_recommendations(user_data))
        
        # Add study sessions table
        story.extend(self._create_sessions_table(user_data))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer.getvalue()
    
    def _create_header(self, username, period):
        """Create PDF header with title and user information"""
        story = []
        
        # Main title
        title = Paragraph("⏏︎ Elevate - Progress Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # User and period information
        user_info = f"<b>Student:</b> {username}<br/><b>Report Period:</b> {period}<br/><b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        user_para = Paragraph(user_info, self.normal_style)
        story.append(user_para)
        story.append(Spacer(1, 30))
        
        return story
    
    def _create_executive_summary(self, user_data, quiz_data):
        """Create executive summary section"""
        story = []
        
        story.append(Paragraph("⏏︎ Executive Summary", self.subtitle_style))
        
        if user_data.empty:
            story.append(Paragraph("No study data available for this period.", self.normal_style))
            return story
        
        # Calculate key metrics
        total_time = user_data['duration_minutes'].sum()
        total_sessions = len(user_data)
        avg_confidence = user_data['confidence_rating'].mean()
        unique_subjects = user_data['subject'].nunique()
        unique_chapters = user_data['chapter'].nunique()
        
        # Quiz metrics
        quiz_summary = ""
        if quiz_data is not None and not quiz_data.empty:
            avg_quiz_score = quiz_data['score'].mean()
            total_quizzes = len(quiz_data)
            quiz_summary = f"<br/>• <b>Quizzes Taken:</b> {total_quizzes}<br/>• <b>Average Quiz Score:</b> {avg_quiz_score:.1f}%"
        
        summary_text = f"""
        <b>Study Overview:</b><br/>
        • <b>Total Study Time:</b> {format_time(total_time)}<br/>
        • <b>Study Sessions:</b> {total_sessions}<br/>
        • <b>Average Confidence:</b> {avg_confidence:.1f}/5<br/>
        • <b>Subjects Studied:</b> {unique_subjects}<br/>
        • <b>Chapters Covered:</b> {unique_chapters}{quiz_summary}
        """
        
        story.append(Paragraph(summary_text, self.normal_style))
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_detailed_statistics(self, user_data, quiz_data):
        """Create detailed statistics section"""
        story = []
        
        story.append(Paragraph("⏏︎ Detailed Statistics", self.subtitle_style))
        
        if user_data.empty:
            return story
        
        # Study patterns
        story.append(Paragraph("Study Patterns", self.header_style))
        
        # Daily average
        unique_days = user_data['date'].nunique()
        daily_avg = user_data['duration_minutes'].sum() / unique_days if unique_days > 0 else 0
        
        # Session length analysis
        avg_session = user_data['duration_minutes'].mean()
        longest_session = user_data['duration_minutes'].max()
        shortest_session = user_data['duration_minutes'].min()
        
        patterns_text = f"""
        • <b>Daily Average Study Time:</b> {format_time(daily_avg)}<br/>
        • <b>Average Session Length:</b> {avg_session:.1f} minutes<br/>
        • <b>Longest Session:</b> {longest_session} minutes<br/>
        • <b>Shortest Session:</b> {shortest_session} minutes<br/>
        • <b>Active Study Days:</b> {unique_days}
        """
        
        story.append(Paragraph(patterns_text, self.normal_style))
        story.append(Spacer(1, 15))
        
        # Confidence analysis
        story.append(Paragraph("Confidence Analysis", self.header_style))
        
        confidence_dist = user_data['confidence_rating'].value_counts().sort_index()
        confidence_text = "<b>Confidence Rating Distribution:</b><br/>"
        for rating, count in confidence_dist.items():
            percentage = (count / len(user_data)) * 100
            stars = "⭐" * rating
            confidence_text += f"• {rating} {stars}: {count} sessions ({percentage:.1f}%)<br/>"
        
        story.append(Paragraph(confidence_text, self.normal_style))
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_subject_breakdown(self, user_data):
        """Create subject breakdown section"""
        story = []
        
        story.append(Paragraph("⏏︎ Subject Breakdown", self.subtitle_style))
        
        if user_data.empty:
            return story
        
        # Group by subject
        subject_stats = user_data.groupby('subject').agg({
            'duration_minutes': ['sum', 'count', 'mean'],
            'confidence_rating': ['mean', 'std']
        }).round(2)
        
        # Flatten column names
        subject_stats.columns = ['Total_Time', 'Sessions', 'Avg_Session', 'Avg_Confidence', 'Confidence_Std']
        subject_stats = subject_stats.reset_index()
        
        # Create table data
        table_data = [['Subject', 'Total Time', 'Sessions', 'Avg Session', 'Avg Confidence']]
        
        for _, row in subject_stats.iterrows():
            table_data.append([
                row['subject'],
                format_time(row['Total_Time']),
                str(int(row['Sessions'])),
                f"{row['Avg_Session']:.1f} min",
                f"{row['Avg_Confidence']:.1f}/5"
            ])
        
        # Create table
        table = Table(table_data, colWidths=[1.5*inch, 1*inch, 0.8*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_performance_analysis(self, user_data):
        """Create performance analysis section"""
        story = []
        
        story.append(Paragraph("⏏︎ Performance Analysis", self.subtitle_style))
        
        if user_data.empty or len(user_data) < 3:
            story.append(Paragraph("Insufficient data for performance analysis. Continue studying to see trends!", self.normal_style))
            return story
        
        # Trend analysis
        story.append(Paragraph("Confidence Trends", self.header_style))
        
        # Calculate trend for each subject
        trend_analysis = []
        for subject in user_data['subject'].unique():
            subject_data = user_data[user_data['subject'] == subject].sort_values('date')
            if len(subject_data) >= 3:
                # Simple trend calculation
                first_third = subject_data.iloc[:len(subject_data)//3]['confidence_rating'].mean()
                last_third = subject_data.iloc[-len(subject_data)//3:]['confidence_rating'].mean()
                trend = last_third - first_third
                
                trend_analysis.append({
                    'subject': subject,
                    'trend': trend,
                    'current_confidence': last_third
                })
        
        if trend_analysis:
            trends_text = ""
            for item in trend_analysis:
                trend_icon = "📈" if item['trend'] > 0.2 else "📉" if item['trend'] < -0.2 else "➡️"
                trend_desc = "improving" if item['trend'] > 0.2 else "declining" if item['trend'] < -0.2 else "stable"
                trends_text += f"• <b>{item['subject']}:</b> {trend_icon} {trend_desc} (Current: {item['current_confidence']:.1f}/5)<br/>"
            
            story.append(Paragraph(trends_text, self.normal_style))
        
        story.append(Spacer(1, 15))
        
        # Identify strengths and weaknesses
        story.append(Paragraph("Strengths and Areas for Improvement", self.header_style))
        
        chapter_performance = user_data.groupby(['subject', 'chapter'])['confidence_rating'].mean()
        
        # Top performing chapters
        top_chapters = chapter_performance.nlargest(3)
        weak_chapters = chapter_performance.nsmallest(3)
        
        strengths_text = "<b>⏏︎ Top Performing Areas:</b><br/>"
        for (subject, chapter), confidence in top_chapters.items():
            strengths_text += f"• {subject} - {chapter}: {confidence:.1f}/5<br/>"
        
        weaknesses_text = "<br/><b>⏏︎ Areas Needing Attention:</b><br/>"
        for (subject, chapter), confidence in weak_chapters.items():
            if confidence < 3.5:  # Only show if actually weak
                weaknesses_text += f"• {subject} - {chapter}: {confidence:.1f}/5<br/>"
        
        story.append(Paragraph(strengths_text, self.normal_style))
        story.append(Paragraph(weaknesses_text, self.highlight_style))
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_recommendations(self, user_data):
        """Create recommendations section"""
        story = []
        
        story.append(Paragraph("⏏︎ Personalized Recommendations", self.subtitle_style))
        
        recommendations = []
        
        if user_data.empty:
            recommendations.append("Start logging your study sessions to receive personalized recommendations!")
        else:
            # Analyze study patterns and generate recommendations
            
            # Check study consistency
            unique_days = user_data['date'].nunique()
            date_range = (pd.to_datetime(user_data['date'].max()) - pd.to_datetime(user_data['date'].min())).days + 1
            consistency_ratio = unique_days / date_range if date_range > 0 else 1
            
            if consistency_ratio < 0.5:
                recommendations.append("⏏︎ Try to study more consistently. Aim for at least 4-5 study sessions per week.")
            
            # Check session length
            avg_session = user_data['duration_minutes'].mean()
            if avg_session < 20:
                recommendations.append("⏏︎ Consider longer study sessions (20-45 minutes) for better focus and retention.")
            elif avg_session > 90:
                recommendations.append("⏏︎ Break down very long sessions into smaller chunks with breaks for better effectiveness.")
            
            # Check confidence levels
            low_confidence_subjects = user_data.groupby('subject')['confidence_rating'].mean()
            weak_subjects = low_confidence_subjects[low_confidence_subjects < 3.0]
            
            if len(weak_subjects) > 0:
                subject_list = ", ".join(weak_subjects.index[:3])
                recommendations.append(f"⏏︎ Focus extra attention on: {subject_list}. Consider seeking additional resources or help.")
            
            # Check subject diversity
            subject_count = user_data['subject'].nunique()
            if subject_count == 1:
                recommendations.append("⏏︎ Consider diversifying your study subjects to maintain engagement and prevent burnout.")
            
            # Time-based recommendations
            total_time = user_data['duration_minutes'].sum()
            if total_time < 300:  # Less than 5 hours total
                recommendations.append("⚡ Increase your study time gradually. Consistent daily practice leads to better results.")
            
            if not recommendations:
                recommendations.append("⏏︎ Excellent study habits! Keep maintaining your current routine and continue tracking your progress.")
        
        recommendations_text = ""
        for i, rec in enumerate(recommendations[:6], 1):  # Limit to 6 recommendations
            recommendations_text += f"{i}. {rec}<br/><br/>"
        
        story.append(Paragraph(recommendations_text, self.normal_style))
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_sessions_table(self, user_data):
        """Create detailed sessions table"""
        story = []
        
        story.append(Paragraph("⏏︎  Recent Study Sessions", self.subtitle_style))
        
        if user_data.empty:
            story.append(Paragraph("No study sessions recorded.", self.normal_style))
            return story
        
        # Get recent sessions (last 20)
        recent_sessions = user_data.tail(20)
        
        # Create table data
        table_data = [['Date', 'Subject', 'Chapter', 'Duration', 'Confidence']]
        
        for _, session in recent_sessions.iterrows():
            table_data.append([
                str(session['date']),
                session['subject'],
                session['chapter'][:25] + '...' if len(session['chapter']) > 25 else session['chapter'],
                f"{session['duration_minutes']} min",
                f"{session['confidence_rating']}/5"
            ])
        
        # Create table
        table = Table(table_data, colWidths=[1*inch, 1.2*inch, 1.8*inch, 0.8*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Add footer
        footer_text = f"<i>Report generated by Elevate on {datetime.now().strftime('%B %d, %Y')}</i>"
        footer = Paragraph(footer_text, ParagraphStyle('Footer', parent=self.styles['Normal'], 
                                                      fontSize=8, alignment=TA_CENTER, 
                                                      textColor=colors.grey))
        story.append(footer)
        
        return story
