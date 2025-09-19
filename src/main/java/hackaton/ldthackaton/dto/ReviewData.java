package hackaton.ldthackaton.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class ReviewData {
    @NotNull(message = "ID отзыва не может быть null")
    private Long id;

    @NotNull(message = "Текст отзыва не может быть null")
    private String text;
}