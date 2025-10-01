package hackaton.ldthackaton.controller;

import hackaton.ldthackaton.dto.RatingStatsDto;
import hackaton.ldthackaton.dto.ThemeDto;
import hackaton.ldthackaton.dto.TonalityStatsDto;
import hackaton.ldthackaton.dto.TotalTonalityDto;
import hackaton.ldthackaton.service.DashboardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api")
public class DashboardController {

    @Autowired
    private DashboardService dashboardService;

    @GetMapping("/themes")
    public List<ThemeDto> getThemes() {
        return dashboardService.getAllThemes();
    }

    @GetMapping("/rating-stats")
    public List<RatingStatsDto> getRatingStats() {
        return dashboardService.getRatingStats();
    }

    @GetMapping("/sentiment-stats")
    public List<TonalityStatsDto> getSentimentStats() {
        return dashboardService.getSentimentStatsByMonth();
    }

    @GetMapping("/sentiment-total")
    public TotalTonalityDto getTotalSentiment() {
        return dashboardService.getTotalSentiment();
    }
}