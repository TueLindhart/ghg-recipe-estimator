This file will contain the project description for redesign of estimate page. 

The project is described using images where images matching current-*.PNG are images from current layout. 

Otherwise, images are sketched of new layout is wanted. 

Changes:

- Overview card should show `co2_per_person_kg` with a much greater font size where it below with smaller font; "{total_co2_kg} kg CO2e for {number_of_persons} personer". 
- Below overview card in mobile and left to in desktop screens should be three tabs: Sammenlign, Svare til and Næringsindhold:
  - "Sammenlign" should show how `co2_per_person_kg` number is wrt. to `budget_emission_per_person_per_meal` in pct and `budget_emission_per_person_per_day` in pc + `avg_emission_per_person_per_meal` in pct. Percent number should be in great font size and bold. text should be smaller and respectively say "af dit budget per måltid på 0.5 kg CO2", "af dagligt budget på 2 kg CO2" and "af en gennemsnitsdanskers måltid på 1.75 kg CO2". 
  - "Svare til" should show comparisons to how many kilometers it would be in a car, how many times you can eat that meal for it equals a flight from Copenhagen to London and finally how many hours you can run a washingmachine. 
  - "Næringsindhold" displays energy_per_person_kj, fat_per_person_g, carbohydrate_per_person_g and protein_per_person_g where fat, carbohydrate and protein are shown in a barchart and energy is shown bold big letters left for batchart. 
- Below Overview card and tabs we have another tab element with two tabs as we know it which are: "Ingredienser" and "Graf"
  - "Ingredienser" displays the additional energy_kj, fat_g, carbohydrate_g and protein_g elements we have per ingredient. 
  - "Graf" have a dropdown menu (that default to CO2e kg) but you can also choose energy, protein, carbohydrate and fat. 

Description of images:
- overview+sammenlign-tab.jpeg shows sketch of overview card and "Sammenlign" card. 
- svare-til-tab.jpeg shows sketch of "Svare til" tab. 
- "næringsindhold.jpeg" shows sketch of "Næringsindhold" tab. 
- "ingredienser-and-graf-tab.jpeg" shows sketch of "Ingredienser" and "graf" tabs. 

