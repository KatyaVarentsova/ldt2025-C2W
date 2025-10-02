package hackaton.ldthackaton.dto;

public class ThemeDto {
    private Integer idCategory;
    private String themeCategory;

    public ThemeDto(Integer idCategory, String themeCategory) {
        this.idCategory = idCategory;
        this.themeCategory = themeCategory;
    }


    public Integer getIdCategory() { return idCategory; }
    public String getThemeCategory() { return themeCategory; }
}
