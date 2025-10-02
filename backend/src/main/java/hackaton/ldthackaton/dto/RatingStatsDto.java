package hackaton.ldthackaton.dto;

public class RatingStatsDto {
    private Integer year;
    private String month;
    private int monthNumber;
    private Integer star1 = 0;
    private Integer star2 = 0;
    private Integer star3 = 0;
    private Integer star4 = 0;
    private Integer star5 = 0;

    public int getMonthNumber() {
        return monthNumber;
    }

    public void setMonthNumber(int monthNumber) {
        this.monthNumber = monthNumber;
    }

    public Integer getYear() { return year; }
    public void setYear(Integer year) { this.year = year; }

    public String getMonth() { return month; }
    public void setMonth(String month) { this.month = month; }

    public Integer getStar1() { return star1; }
    public void setStar1(Integer star1) { this.star1 = star1; }

    public Integer getStar2() { return star2; }
    public void setStar2(Integer star2) { this.star2 = star2; }

    public Integer getStar3() { return star3; }
    public void setStar3(Integer star3) { this.star3 = star3; }

    public Integer getStar4() { return star4; }
    public void setStar4(Integer star4) { this.star4 = star4; }

    public Integer getStar5() { return star5; }
    public void setStar5(Integer star5) { this.star5 = star5; }

}