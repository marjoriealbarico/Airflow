CREATE TABLE IF NOT EXISTS urgences_covid (
    id serial PRIMARY KEY,
    dep INT,
    date_de_passage DATE,
    sursaud_cl_age_corona INT,
    nbre_pass_corona INT,
    nbre_pass_tot INT,
    nbre_hospit_corona INT,
    nbre_pass_corona_h INT,
    nbre_pass_corona_f INT,
    nbre_pass_tot_h INT,
    nbre_pass_tot_f INT,
    nbre_hospit_corona_h INT,
    nbre_hospit_corona_f INT,
    CONSTRAINT fk_departments_region FOREIGN KEY (dep) REFERENCES departments_region(num_dep),
    CONSTRAINT fk_tranche_age FOREIGN KEY (sursaud_cl_age_corona) REFERENCES tranche_age(code)
);
