package hackaton.ldthackaton.dto;

import lombok.Data;

import java.util.List;

@Data
public class PredictionResponse {
    private List<ReviewPrediction> predictions;
}
