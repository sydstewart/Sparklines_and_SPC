import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server
from anvil.pdf import PDFRenderer

# @anvil.server.callable
# def create_pdf():
#   media_object = anvil.pdf.render_form('Form2', 42, name='Zaphod')
#   return media_object

@anvil.server.callable
def send_pdf_email_sales():
  anvil.email.send(
    from_name="The Zaphod Generator", 
    to="sydney.w.stewart@gmail.com", 
    subject="An auto-generated Zaphod",
    text="Your auto-generated Zaphod is attached to this email as a PDF.",
    attachments =anvil.pdf.render_form('sales_sparklines')
  )
@anvil.server.callable
def send_pdf_email_support():
  pdf = PDFRenderer(page_size='A4', landscape = True).render_form('support_dashboard')
  anvil.email.send(
    from_name="The Zaphod Generator", 
    to="sydney.w.stewart@gmail.com", 
    subject="An auto-generated Zaphod",
    text="Your auto-generated Zaphod is attached to this email as a PDF.",
    attachments= pdf  # anvil.pdf.render_form('support_dashboard')  
     

  
  )
@anvil.server.callable
def send_pdf_email_sales_step_changes():
  """Launch a single crawler background task."""
  task = anvil.server.launch_background_task('send_pdf_email_sales_step_changes_background')

  if task.is_completed():
     
     return task
  
@anvil.server.callable
def send_pdf_email_sales_step_changes_background():
  pdf = PDFRenderer(page_size='A4', landscape = True).render_form('Stacked_Sales_Charts')
  anvil.email.send(
    from_name="Syd Stewart", 
    to="sydney.w.stewart@gmail.com", 
    subject="Stacked Sales Charts",
    text="Your auto-generated Sales Step Charts is attached to this email as a PDF.",
    attachments =anvil.pdf.render_form('Stacked_Sales_Charts')
  )
  
@anvil.server.callable
def send_pdf_email_support_sparks():
  pdf = PDFRenderer(page_size='A4', landscape = True).render_form('support_sparklines')
  anvil.email.send(
    from_name="Support Sparklines", 
    to="sydney.w.stewart@gmail.com", 
    subject="Support Sparklines",
    text="Please find a support sparklines dashboard attached to this email as a PDF.",
    attachments= pdf #anvil.pdf.render_form('support_sparklines')  
  )

@anvil.server.callable
def create_zaphod_pdf():
  media_object = anvil.pdf.render_form('Form2')
  return media_object