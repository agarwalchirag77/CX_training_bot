import openai
import pandas as pd
import difflib


with open('/Users/hevo/Downloads/testquery.txt', 'r') as file:
    documentation_text = file.read()

aboutHevo='https://docs.hevodata.com/introduction/about-hevo/'
# Similarity threshold to control uniqueness
similarity_threshold = 0.5


num_questions = 15
responses = []
previous_questions = set()

# Run a loop for generating queries and receiving responses
while len(responses) < num_questions:
    # Generate multiple queries using OpenAI's completion endpoint
    sample_query_prompt = f'''You are a chatbot acting as a customer with doubts about Hevo Data. 
    Hevo is a no-code data movement platform that is usable by your most technical as well as your non-technical and business users. Hevo's near real-time data movement platform simplifies the data integration challenges in any data analytics project. Using the Hevo platform, you can set up a database or a data warehouse and analyze your data with minimal effort. Simply put, Hevo allows you to shift focus from data integration to analytics.
    
    Hevo's multi-tenant platform leverages several components of Amazon's AWS cloud for its infrastructure. The platform is designed to process billions of records and can automatically scale up or down based on workload needs. Hevo's architecture ensures the optimum usage of system resources so that you get the best return on your investment.
    
    Hevo's intuitive user interface makes it easy for technical and non-technical resources to set up and manage your data Pipelines. Hevo's design approach goes beyond data Pipelines. Its analyst-friendly data transformation features are well integrated into the platform to streamline the analytics tasks further.
    
    Hevo supports 150+ ready-to-use integrations across databases, SaaS Applications, cloud storage, SDKs, and streaming services. With just a five-minute setup, you can replicate data from any of these Sources to a database or data warehouse Destination of your choice.
    
    On the one hand, with the powerful Python code-based and drag-and-drop Transformations, you can cleanse and prepare the data to be loaded to your Destination. While on the other hand, Models and Workflows can help you get the loaded data in an analysis-ready form.
    
    The assistance built into the product is prompt, preemptive, and smart. It provides you with complete visibility and control over your data while helping you reduce costs.
    
    Hevo offers a transparent, usage-based pricing model. You can select from one of its Free, Starter, or Business plans based on your needs. Hevo also allows you to try the product free for 14 days with its Free and Starter plans. You can purchase On-Demand Events or set up On-Demand Credit to handle any overages so that your data continues to load without interruption. and Feel free to consult the document {documentation_text} when crafting your questions. Please ensure that your question is unique, elaborative should not be yes or no type questions and hasn't been asked before. Previous questions: {', '.join(previous_questions)} and just need to ask a question without attaching anything to the question like question number or question. 

    Remember, ask only one question at a time, and please refrain from providing answers. Just record the responses.'''
    
    sample_query_response = openai.Completion.create(
        engine="text-davinci-003", #https://platform.openai.com/docs/models/gpt-3-5   4,097 tokens	
        prompt=sample_query_prompt,
        temperature=0.7,  # Adjust the temperature value
        max_tokens=1000,
        n=5  # Generate 5 queries in a single API call
    )
    print(str(sample_query_response))
    # Filter and record the unique queries
    for choice in sample_query_response.choices:
        sample_query = choice.text.strip()

        # Check if the question is unique and meets the criteria
        is_unique = all([
            sample_query not in previous_questions,
            '?' in sample_query,
            'yes' not in sample_query.lower(),
            'no' not in sample_query.lower()
        ])
        
        if is_unique:
            ans = input(f"Query: {sample_query}\nYour Response: ")
            # Record the query and response
            responses.append({'query': sample_query, 'ans': ans})
            previous_questions.add(sample_query)

df = pd.DataFrame(responses)
df.to_csv('responses.csv', index=False)

print(responses)
