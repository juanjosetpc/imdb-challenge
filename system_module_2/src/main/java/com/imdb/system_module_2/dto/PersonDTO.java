package com.imdb.system_module_2.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PersonDTO {
    private String name;
    private Integer birthYear;
    private Integer deathYear;
    private String profession;
}
