package com.imdb.system_module_2.mapper;

import com.imdb.system_module_2.dto.FilmDTO;
import com.imdb.system_module_2.entity.Film;

public class FilmMapper {
    public static FilmDTO toDTO(Film movie) {
        FilmDTO dto = new FilmDTO();
        dto.setTitle(movie.getPrimaryTitle());
        dto.setOriginalTitle(movie.getOriginalTitle());
        dto.setType(movie.getTitleType());
        dto.setYear(movie.getStartYear());
        return dto;
    }
}
