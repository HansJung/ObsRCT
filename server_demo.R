library(shiny)
library(scidb)
scidbconnect()

# R code for Use case three
# Cohort selection and data visualization based on drug usage
shinyServer(function(input, output) {
  require("RPostgreSQL")
  # save the password that we can "hide" it as best as we can by collapsing it
  pw <- {
    "mimic"
  }
  # loads the PostgreSQL driver
  drv <- dbDriver("PostgreSQL")
  # creates a connection to the postgres database
  # note that "con" will be used later in each connection to the database
  con <- dbConnect(drv, dbname = "mimic",
                   host = "localhost", port = 5433,
                   user = "mimic", password = pw)
  # removes the password
  rm(pw) 
  
  # Query the database for a list of all antidepressant drugs
  query_drugs = "SELECT drug, COUNT(DISTINCT(subject_id)) 
    		FROM mimiciii.prescriptions 
    		WHERE drug LIKE '%Amitriptyline%' 
    		  OR drug LIKE '%Amoxapine%' 
    		  OR drug LIKE '%Clomipramine%' 
    		  OR drug LIKE '%Desipramine%'
    		  OR drug LIKE '%Dothiepin%'
    		  OR drug LIKE '%Doxepin%'
    		  OR drug LIKE '%Imipramine%'
    		  OR drug LIKE '%Lofepramine%'
    		  OR drug LIKE '%Nortriptyline%'
    		  OR drug LIKE '%Protriptyline%' 
    		  OR drug LIKE '%Trimipramine%' 
    		GROUP BY drug;"
  data_antidepressants = dbGetQuery(con,query_drugs)
  
  # Populate a table with a list of antidepressant drugs
  output$tblAntidepressant <- DT::renderDataTable({
    data_antidepressants
  }, rownames=TRUE, server=TRUE)
  
  # Query the database for a list of all antihistamine drugs
  query_antihistamines = "SELECT drug, COUNT(DISTINCT(subject_id)) 
			 FROM mimiciii.prescriptions 
			 WHERE drug LIKE '%Dexbrompheniramine%' 
  			 OR drug LIKE '%Dexchlorpheniramine%' 
			   OR drug LIKE '%Dimenhydrinate%' 
			   OR drug LIKE '%Dimethindene%'
			   OR drug LIKE '%Diphenhydramine%'
			   OR drug LIKE '%Diphenylpraline%'
			   OR drug LIKE '%Doxylamine%'
			   OR drug LIKE '%Flunarizine%'
			   OR drug LIKE '%Hydroxyzine%'
			   OR drug LIKE '%Loratadine%' 
			   OR drug LIKE '%Meclizine%'
			   OR drug LIKE '%Methdilazine%'
			   OR drug LIKE '%Phenindamine%'
			   OR drug LIKE '%Pheniramine%'
			   OR drug LIKE '%Phenyltoloxamine%'
			   OR drug LIKE '%Pyrilamine%'
			   OR drug LIKE '%Trimeprazine%'
			   OR drug LIKE '%Tripelennamine%'
			   OR drug LIKE '%Triprolidine%'
			 GROUP BY drug;"
  data_antihistamines = dbGetQuery(con,query_antihistamines)

  #Populate a table with a list of antihistamine drugs
  output$tblAntihistamine <- DT::renderDataTable({
    data_antihistamines
  }, rownames=TRUE, server=TRUE)
  

  #Display list of drugs selected from either list
  output$txtSelectedDrugs <- renderPrint({
    antiDepressantSelected <- input$tblAntidepressant_rows_selected
    antiHistamineSelected <- input$tblAntihistamine_rows_selected
    cat(data_antidepressants[as.numeric(antiDepressantSelected), c("drug")], sep = "\n")
    cat(data_antihistamines[as.numeric(antiHistamineSelected), c("drug")], sep = "\n")
  })
  
  
  #Run when 'Analyze Cohort' button is clicked
  #Generates message notification based on selected drugs
  selectedAllDrugs <- eventReactive(input$analyzeCohort,{
    antiDepressantSelected <- input$tblAntidepressant_rows_selected
    antiHistamineSelected <- input$tblAntihistamine_rows_selected

    if(length(antiDepressantSelected)+length(antiHistamineSelected)==2){
      data_patients <- get_cohort()
      if(is.null(data_patients)){
        notification <- "No data found with this combination of drugs."
      }else{
        notification <- paste(nrow(data_patients)," rows retrieved with this combination of drugs.")
      }
    }else{
      notification <- "Exactly two drugs must be selected for analysis."
    }
    notification
  })


  #Display message notification
  output$txtDrugs <- renderPrint({
    cat(selectedAllDrugs())
  })
  

  #Query database for data when selected drugs were used in combination
  #Return data frame of results.
  get_cohort <- reactive({
    antiDepressantSelected <- input$tblAntidepressant_rows_selected
    antiHistamineSelected <- input$tblAntihistamine_rows_selected

    if (length(antiDepressantSelected)==1){
       sql_query<- paste0("SELECT T1.subject_id, T1.drug, T1.startdate, T1.enddate, T2.drug, T2.startdate, T2.enddate
                           FROM mimiciii.prescriptions T1, mimiciii.prescriptions T2
                           WHERE T1.subject_id = T2.subject_id
                             AND (T1.startdate, T1.enddate) OVERLAPS (T2.startdate, T2.enddate)
                             AND T1.drug LIKE '",data_antidepressants[antiDepressantSelected[[1]],c("drug")],"'
                             AND T2.drug LIKE '",data_antihistamines[antiHistamineSelected[[1]],c("drug")],"'")
    }else if(length(antiDepressantSelected)==2){
        sql_query<- paste0("SELECT T1.subject_id, T1.drug, T1.startdate, T1.enddate, T2.drug, T2.startdate, T2.enddate
                           FROM mimiciii.prescriptions T1, mimiciii.prescriptions T2
                           WHERE T1.subject_id = T2.subject_id
                             AND (T1.startdate, T1.enddate) OVERLAPS (T2.startdate, T2.enddate)
                             AND T1.drug LIKE '",data_antidepressants[antiDepressantSelected[[1]],c("drug")],"'
                             AND T2.drug LIKE '",data_antidepressants[antiDepressantSelected[[2]],c("drug")],"'")
    }else if(length(antiHistamineSelected)==2) {
        sql_query<- paste0("SELECT T1.subject_id, T1.drug, T1.startdate, T1.enddate, T2.drug, T2.startdate, T2.enddate
                           FROM mimiciii.prescriptions T1, mimiciii.prescriptions T2
                           WHERE T1.subject_id = T2.subject_id
                             AND (T1.startdate, T1.enddate) OVERLAPS (T2.startdate, T2.enddate)
                             AND T1.drug LIKE '",data_antihistamines[antiHistamineSelected[[1]],c("drug")],"'
                             AND T2.drug LIKE '",data_antihistamines[antiHistamineSelected[[2]],c("drug")],"'")
    }
    
    data_patients = dbGetQuery(con,sql_query)
  })


  #Display drug combination data retrieved in get_cohort function. 
  #Update only when Analyze Cohort button is clicked.
  output$tblCohort <- DT::renderDataTable({
    input$analyzeCohort
    antiDepressantSelected <- isolate(input$tblAntidepressant_rows_selected)
    antiHistamineSelected <- isolate(input$tblAntihistamine_rows_selected)

    if(length(antiDepressantSelected)+length(antiHistamineSelected)==2){
      data_patients<-isolate(get_cohort())
      data_patients
    }
  }, rownames=TRUE, server=TRUE, selection = 'single')

  #Display plots of patient data for selected cohort row
  output$subjectSystolicPlot <-renderPlot({
    req(input$tblCohort_rows_selected)

    data_patients<-get_cohort()
    selected_presc <- input$tblCohort_rows_selected
  
    #Extract data from selected row
    subject_id <- data_patients[as.numeric(selected_presc[[1]]),1]
    start_date_1 <-data_patients[as.numeric(selected_presc[[1]]),3]
    end_date_1 <-data_patients[as.numeric(selected_presc[[1]]),4]
    
    start_date_2 <-data_patients[as.numeric(selected_presc[[1]]),6]
    end_date_2 <-data_patients[as.numeric(selected_presc[[1]]),7]

    #Get info from data for selected subject and date range
    #ENTER QUERY HERE    
    query_gender <-paste0("select gender from mimiciii.patients where subject_id = ", subject_id)
    data_gender <- dbGetQuery(con, query_gender)
    query_age <- paste0("WITH first_admission_time AS
                        (
                        SELECT
                        p.subject_id, p.dob, p.gender
                        , MIN (a.admittime) AS first_admittime
                        , MIN( ROUND( (cast(admittime as date) - cast(dob as date)) / 365.242,2) )
                        AS first_admit_age
                        FROM mimiciii.patients p
                        INNER JOIN mimiciii.admissions a
                        ON p.subject_id = a.subject_id
                        GROUP BY p.subject_id, p.dob, p.gender
                        ORDER BY p.subject_id
                        )
                        SELECT
                        subject_id, dob, gender
                        , first_admittime, first_admit_age
                        , CASE
                        -- all ages > 89 in the database were replaced with 300
                        WHEN first_admit_age > 89
                        then '>89'
                        WHEN first_admit_age >= 14
                        THEN 'adult'
                        WHEN first_admit_age <= 1
                        THEN 'neonate'
                        ELSE 'middle'
                        END AS age_group
                        FROM first_admission_time where subject_id='",subject_id,"'")
    data_age <- dbGetQuery(con,query_age)
   
    output$txtSubject <- renderPrint({
      
      cat(paste0("Gender: ", data_gender,"\n"))
      cat(paste0("Age: ", data_age[["first_admit_age"]],"\n"))
      
      
    })  
    query_subject_chartevents <-paste0("select  charttime, mimiciii.chartevents.subject_id as subject, mimiciii.chartevents.valuenum as value, mimiciii.d_items.itemid as itemid, mimiciii.d_items.label
                  from mimiciii.chartevents,mimiciii.d_items 
                              where mimiciii.chartevents.subject_id = ",subject_id," and
                              mimiciii.chartevents.itemid = mimiciii.d_items.itemid and
                              mimiciii.chartevents.valuenum is not null and
                                                            mimiciii.chartevents.charttime between least(date('",start_date_1,"'),date('",start_date_2,"')) and greatest(date('",end_date_1,"'), date ('",end_date_2,"')) order by charttime")
   
    data_subject_chartevents <-dbGetQuery(con,query_subject_chartevents)
    output$tblChartevents <- DT::renderDataTable({
      data_subject_chartevents
    }, rownames=TRUE, server=TRUE)
    systolic_bp <- data_subject_chartevents[data_subject_chartevents$itemid %in% '455', ] #item id for NBP [Systolic] = 455

    output$tblSystolic <- DT::renderDataTable({
      systolic_bp
    }, rownames=TRUE, server=TRUE)

    plot(systolic_bp[["charttime"]],systolic_bp[["value"]], main = "Systolic BP", xlab = "Time(hr)", ylab= "Systolic BP")
    lines(systolic_bp[["charttime"]],systolic_bp[["value"]],col="red")
    
    heart_rate <- data_subject_chartevents[data_subject_chartevents$itemid %in% '211', ] #item id for Hear Rate = 211
    
     output$tblHR <- DT::renderDataTable({
       heart_rate
     }, rownames=TRUE, server=TRUE)

     output$subjectHRPlot <- renderPlot({
       plot(heart_rate[["charttime"]],heart_rate[["value"]], main = "Heart Rate", xlab = "Time(hr)", ylab= "Heart Rate")
       lines(heart_rate[["charttime"]],heart_rate[["value"]],col="red")
     })


    # 
    
    # 
    # plot(1:length(heart_rate[["value"]]),heart_rate[["value"]], main = "Heart Rate", xlab = "Time(min)", ylab= "Heart Rate")
    # lines(1:length(heart_rate[["value"]]),heart_rate[["value"]],col="green")
    # 
    # plot(1:length(data_subject_hr[["hr"]]),data_subject_hr[["hr"]],main="HR", xlab = "Time(hr)", ylab = "HR")
    # lines(1:length(data_subject_hr[["hr"]]),data_subject_hr[["hr"]],col="red")
  })

})
