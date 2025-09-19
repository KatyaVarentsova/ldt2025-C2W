package hackaton.ldthackaton.dto;
import lombok.Data;

import java.util.List;

@Data
public class ReviewPrediction {
    private Long id;
    private List<String> topics;
    private List<String> sentiments;
}