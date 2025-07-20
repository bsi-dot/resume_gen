Generate_resume.py
  Inputs YAML resume data with the TEX template to generate the resume
  Inputs: 
      simple_boilerplate.tex -> Tex Generic Template File 
      simple_data.yaml -> YAML Resume Data file 
  Output: 
      simple_output.pdf -> pdf      
      simple_output.tex -> tex

logic_match.py       
  Inputs the Config file with the resume yaml. The output of this will be fed to as the simple_data.yaml to be used by 
  the Generate_resume Module above
  Inputs: 
      config.yaml -> Config File for logic match 
      full_resume.yaml -> The Full Resume File
      job_description.txt -> JD File to compare
    
  
