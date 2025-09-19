package hackaton.ldthackaton.dto;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.util.List;

@Data
public class PredictionRequest {
    @NotEmpty(message = "Список отзывов не может быть пустым")
    @Valid
    private List<@NotNull ReviewData> data;
}
