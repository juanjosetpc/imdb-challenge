package com.imdb.system_module_2.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "people")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Person {

    @Id
    @Column(name = "nconst", length = 20)
    private String nconst;

    @Column(name = "primaryName", length = 255)
    private String primaryName;

    @Column(name = "birthYear")
    private Integer birthYear;

    @Column(name = "deathYear")
    private Integer deathYear;

    @Column(name = "primaryProfession", length = 255)
    private String primaryProfession;

    @Column(name = "knownForTitles", columnDefinition = "TEXT")
    private String knownForTitles;
}
