import sys as sys
import re as re
import pandas as pd

def oppl_to_df(company, patent_file):
    """Takes a wide patent file, and returns a pandas DataFrame
    Inputs:
        company: string of company name
        patent_file: .txt file where each patent owned by company is on a single line
    Ouput:
        pandas DataFrame, where rows are patents, and columns are the features:
            company name
            patent assignee
            year granted
            year applied
            patent class
            patent number
            patent title
            patent abstract
    """
    
    # initialize fields as a dictionary
    fields = {'company_name' : [],
              'patent_assignee' : [],
              'year_granted' : [],
              'year_applied' : [],
              'patent_class' : [],
              'patent_number' : [],
              'patent_title' : [],
              'patent_abstract' : []}
    
    # specify regular expressions
    assignee_re = '<assignee>.*?</orgname>'
    pub_ref_re = '<publication-reference>.*?</publication-reference>'
    date_tags = '<publication-reference>.*<date>|</date>.*'
    id_tags = '<publication-reference>.*<doc-number>|</doc-number>.*'
    app_ref_re = '<application-reference.*?</application-reference>'
    class_re = '</classification-locarno>.*?</main-classification>'
    title_re = '<invention-title.*?</invention-title>'
    abstract_re = '<abstract.*?</abstract>'
  
    for line in patent_file.readlines():
        # Use regex to find fields, 
        # and append them to appropriate dictionary value
        
        # attach company name
        fields['company_name'].append(company)
        
        # extract patent assignee
        assignee = re.search(assignee_re, line)
        if assignee:
            patent_assignee = re.sub('<assignee>.*<orgname>|</orgname>', 
                                  '', 
                                  assignee.group())
            fields['patent_assignee'].append(patent_assignee)
        else:
            fields['patent_assignee'].append('None')
            
        # extract year granted and patent number, 
        # both in <publication-reference>
        pub_ref = re.search(pub_ref_re, line)
        if pub_ref:
            year_granted = re.sub(date_tags, '', pub_ref.group())
            patent_number = re.sub(id_tags, '', pub_ref.group())
            fields['year_granted'].append(year_granted[0:4])
            fields['patent_number'].append(patent_number)
        else:
            fields['year_granted'].append('None')
            fields['patent_number'].append('None')
            
        # extract year applied
        app_ref = re.search(app_ref_re, line)
        if app_ref:
            year_applied = re.sub('<application.*<date>|</date>.*',
                                  '',
                                  app_ref.group())
            fields['year_applied'].append(year_applied[0:4])
        else:
            fields['year_applied'].append('None')
        
        # extract patent classification
        classification = re.search(class_re, line)
        if classification:
            patent_class = re.sub('</class.*<main-classification>|</main.*',
                                  '',
                                  classification.group())
            fields['patent_class'].append(patent_class)
        else:
            fields['patent_class'].append('None')
                
        # extract patent title
        title = re.search(title_re, line)
        if title:
            patent_title = re.sub('<invention.*?>|</invention.*',
                                  '',
                                  title.group())
            fields['patent_title'].append(patent_title)
        else:
            fields['patent_title'].append('None')
        
        # extract patent abstract
        abstract_field = re.search(abstract_re, line)
        if abstract_field:
            abstract = re.sub('<abstract.*<p.*?>|</abstract>',
                              '',
                              abstract_field.group())
            fields['patent_abstract'].append(abstract)
        else:
            fields['patent_abstract'].append('None')
            
    # transform dictionary to pandas DataFrame
    return pd.DataFrame(fields)
        
def run():
    # paths to patent files for each company. Each patent is on a single line.
    oppl_hp = open('../oppl_hp.txt')
    
    # define lists of companies, and the patent files for feature extraction loop
    oppl_files = [oppl_hp]
    companies = ['Hewlett-Packard Development Company, L.P.']
    
    # convert each patent file into a tidy pandas data frame
    dfs = [oppl_to_df(companies[i], oppl_files[i]) for i in range(len(companies))]
    
    # concatenate the data frames, and write to .csv
    df_combined = pd.concat(dfs, ignore_index=True)
    df_combined.to_csv('hp.csv', index=False)

if __name__ == "__main__":
    run()