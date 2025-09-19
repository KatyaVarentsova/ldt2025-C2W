package hackaton.ldthackaton.controllerTest;

import hackaton.ldthackaton.client.MLServiceClient;
import hackaton.ldthackaton.dto.PredictionRequest;
import hackaton.ldthackaton.dto.PredictionResponse;
import hackaton.ldthackaton.dto.ReviewData;
import hackaton.ldthackaton.dto.ReviewPrediction;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class PredictionControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private MLServiceClient mlServiceClient;

    @Test
    void shouldReturnPredictionResponse() throws Exception {
        // give
        ReviewData inputReview = new ReviewData();
        inputReview.setId(1L);
        inputReview.setText("Тестовый отзыв");

        PredictionRequest request = new PredictionRequest();
        request.setData(List.of(inputReview));

        ReviewPrediction outputPrediction = new ReviewPrediction();
        outputPrediction.setId(1L);
        outputPrediction.setTopics(List.of("Тестовая тема"));
        outputPrediction.setSentiments(List.of("положительно"));

        PredictionResponse mockResponse = new PredictionResponse();
        mockResponse.setPredictions(List.of(outputPrediction));

        when(mlServiceClient.getPredictions(request)).thenReturn(mockResponse);

        // then
        mockMvc.perform(post("/api/predict")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "data": [
                                    {
                                      "id": 1,
                                      "text": "Тестовый отзыв"
                                    }
                                  ]
                                }
                                """))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.predictions[0].id").value(1))
                .andExpect(jsonPath("$.predictions[0].topics[0]").value("Тестовая тема"));
    }
}