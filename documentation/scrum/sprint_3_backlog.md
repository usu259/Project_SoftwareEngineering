# results

## luca
- presents three UML diagrams.
    - system diagram: three user perspectives (supervisor, worker, customer). one central login process. different views and ations for user types. 
    - class diagram: a "copy" of the initial db diagram. 
    - user activity diagram: on a high-level scope desribing what users could do.
        - supervisor: edit available positions / edit customers and projects / create invoice / data analytics (not further specified)
        - worker: edit daily report
        - customer: view daily report to his adress
    
- **note**: the initial db diagram has a weakness regarding price changes. since prices are "hardcoded" later adjustments affect previous invoices
- for a better collaboration the UML diagrams should be tranlated into a code-based form.

## andrea
--

## willi
--

## further dicussed
- library stack: what python libraries to use to build a working web app (FastAPI, Flask)? UML class diagram relies heavily on library stack.
- docker: dockerize project in the end to deploy from raspi.
- scope: there are many ideas but time available could be scarce. a minimal solution could also involve a local solution (QtPy)

# conclusion
- focus on a working, minimal solution.
    - for now work only **supervisor** and **worker** perspective
    - for now work only **edit available positions** and **create invoice** for supervisor
    - for now work only **edit daily report** for worker
    - leave login aside for now

# next steps
- luca: work the prblem with price adjustments and previous invoices / (have a look into library stack)
- andrea: code based-UML and transform PNG (from luca) into it
- willi: write requirments down to SRS / (have a look into library stack, based on SRS)

