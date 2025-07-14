package com.imdb.system_module_2.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "films")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Film {

    @Id
    @Column(name = "tconst", length = 20)
    private String tconst;

    @Column(name = "titleType", length = 50)
    private String titleType;

    @Column(name = "primaryTitle", length = 1000)
    private String primaryTitle;

    @Column(name = "originalTitle", length = 1000)
    private String originalTitle;

    @Column(name = "isAdult")
    private Boolean isAdult;

    @Column(name = "startYear")
    private Integer startYear;

    @Column(name = "endYear")
    private Integer endYear;

    @Column(name = "runtimeMinutes")
    private Integer runtimeMinutes;

    @Column(name = "genres", length = 255)
    private String genres;
}
