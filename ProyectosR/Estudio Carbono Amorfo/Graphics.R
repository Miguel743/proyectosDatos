sp2_20 <- G_NC3_20
sp3_20 <- G_NC4_20
sp2_58 <- G_NC3_58
sp3_58 <- G_NC4_58

# Heatmap para sp2 en muestra con 20% de sp3

plot_20_sp2 <- ggplot(sp2_20,aes(x = Radius, y = Depth , z = tasa_NC3))+ 
   geom_tile(aes(fill=tasa_NC3))+ 
   theme_bw()+ 
   labs(x =  "Radio (nm)", y = "Depth (nm)")+ 
   scale_fill_gradient2(name ="sp² change (%)(sample 20% sp³)",limits = c(-101,20),  oob = scales::squish,low ="yellow",high = "red",mid = "green", midpoint = -100)+
   theme(axis.title.x = element_text(size = 30, hjust = 0.5))+
   theme(axis.title.y = element_text(size = 30, hjust = 0.5))+
   theme(axis.text = element_text(size= 40))+
   theme(legend.title = element_text(size = 15, face = "italic"))+
   theme(legend.text = element_text(size = 10))+
   coord_cartesian(xlim = c(0,4),ylim = c(-3,6.2))+
   theme(legend.background = element_rect(fill = "aliceblue"))+
   scale_x_continuous(breaks = c(seq(from = 0, to = 4, by = 1)), labels = c(seq(from = 0, to = 4, by = 1)))+
   scale_y_continuous(breaks = c(seq(from = -3, to = 6, by = 1)), labels = c(seq(from = -3, to = 6, by = 1)))+
   theme(legend.text.align = 0.5)+ theme(legend.text.align = 0.9)+
   theme(legend.position = c(0.70, 0.1))

  plot_20_sp2
  ggsave(file = "plot_80_sp²_v08.png", width = 10, height = 16)
  ggsave(file = "plot_80_sp²_v08.pdf", width = 10, height = 16)
  
# Heatmap para sp3 en muestra con 20% de sp3
  
  plot_20_sp3<- ggplot(sp3_20,aes(x = Radius, y = Depth,z = tasa_NC4))+ 
    geom_tile(aes(fill=tasa_NC4))+ theme_bw()+ labs(x =  "Radio (nm)", y = "Depth (nm)")+
    scale_fill_gradient2(name ="sp³ change (%)(sample 20% sp³)",limits = c(-101,20),  oob = scales::squish,low ="yellow",high = "red",mid = "green", midpoint = -100, na.value = "green")+
    theme(axis.title.x = element_text(size = 30, hjust = 0.5))+
    theme(axis.title.y = element_text(size = 30, hjust = 0.5))+
    theme(axis.text = element_text(size= 40))+
    theme(legend.title = element_text(size = 15, face = "italic"))+
    theme(legend.text = element_text(size = 10))+
    coord_cartesian(xlim = c(0,4),ylim = c(-3,6.2))+
    theme(legend.background = element_rect(fill = "aliceblue"))+
    scale_x_continuous(breaks = c(seq(from = 0, to = 4, by = 1)), labels = c(seq(from = 0, to = 4, by = 1)))+
    scale_y_continuous(breaks = c(seq(from = -3, to = 6, by = 1)), labels = c(seq(from = -3, to = 6, by = 1)))+
    theme(legend.text.align = 0.5)+ theme(legend.text.align = 0.9)+
    theme(legend.position = c(0.70, 0.1))
    
  plot_20_sp3
  ggsave(file = "plot_20_sp3_v08.png", width = 10, height = 16)
  ggsave(file = "plot_20_sp3_v08.pdf", width = 10, height = 16)

# Heatmap para sp2 en muestra con 58% de sp3
  
  plot_58_sp2<- ggplot(sp2_58,aes(x = Radius, y = Depth , z = tasa_NC3))+ 
    geom_tile(aes(fill=tasa_NC3))+ 
    theme_bw()+ 
    labs(x =  "Radio (nm)", y = "Depth (nm)") +
    scale_fill_gradient2(name ="sp² change (%) (sample 58% sp³)",limits = c(-101,20), oob = scales::squish,low ="yellow",high = "red", mid = "green", midpoint = -100)+
    theme(axis.title.x = element_text(size = 30, hjust = 0.5))+ 
    theme(axis.title.y = element_text(size = 30, hjust = 0.5))+ 
    theme(axis.text = element_text(size= 40))+ theme(legend.title = element_text(size = 15, face = "italic"))+
    theme(legend.text = element_text(size = 10))+
    coord_cartesian(xlim = c(0,4),ylim = c(-3,6.2))+ 
    theme(legend.background = element_rect(fill = "aliceblue"))+ 
    scale_x_continuous(breaks = c(seq(from = 0 , to = 4, by = 1)), labels = c(seq(from = 0, to = 4, by = 1)))+ 
    scale_y_continuous(breaks = c(seq(from = -3, to = 6, by = 1)), labels = c(seq(from = -3, to = 6, by = 1)))+ 
    theme(legend.text.align = 0.9) +
    theme(legend.position = c(0.70, 0.1))
  
  plot_58_sp2
  ggsave(file = "plot_58_sp2_v08.png", width = 10, height = 16) 
  ggsave(file = "plot_58_sp2_v08.pdf", width = 10, height = 16)
  
# Heatmap para sp3 en muestra con 58% de sp3
  
  plot_58_sp3<- ggplot(sp3_58,aes(x = Radius, y = Depth,z = tasa_NC4))+ 
    geom_tile(aes(fill=tasa_NC4))+ 
    theme_bw()+ 
    labs(x =  "Radio (nm)", y = "Depth (nm)") + 
    scale_fill_gradient2("sp³ change (%)(sample 58% sp³)",limits = c(-101,20), oob = scales::squish,low ="yellow",high = "red", mid = "green", midpoint = -100, na.value = "green")+ 
    theme(axis.title.x = element_text(size = 30, hjust = 0.5))+ 
    theme(axis.title.y = element_text(size = 30, hjust = 0.5))+ 
    theme(axis.text = element_text(size= 40))+ 
    theme(legend.title = element_text(size = 15, face = "italic"))+ 
    theme(legend.text = element_text(size = 10)) + 
    coord_cartesian(xlim = c(0,4),ylim = c(-3,6.2))+ 
    theme(legend.background = element_rect(fill = "aliceblue"))+ 
    scale_x_continuous(breaks = c(seq(from = 0, to = 4, by = 1)), labels = c(seq(from = 0, to = 4, by = 1)))+ 
    scale_y_continuous(breaks = c(seq(from = -3, to = 6, by = 1)), labels = c(seq(from = -3, to = 6, by = 1)))+ 
    theme(legend.text.align = 0.5)+
    theme(legend.position = c(0.70, 0.1))
  
  plot_58_sp3
  ggsave(file = "plot_58_sp3_v08.png", width = 10, height = 16)
  ggsave(file = "plot_58_sp3_v08.pdf", width = 10, height = 16)




vp1 <- viewport(width = 1, height = 1, x = 0.5, y = 0.5)
vp1
plot_20_sp2
plot_20_sp3
plot_58_sp2
plot_58_sp3
pdf("polishing-layout_v08.pdf", width = 17.5, height = 25)
grid.newpage()
pushViewport(viewport(layout = grid.layout(2, 2)))
vplayout <- function(x, y)
  viewport(layout.pos.row = x, layout.pos.col = y)
print(plot_20_sp2, vp = vplayout(1, 1))
print(plot_20_sp3, vp = vplayout(1, 2))
print(plot_58_sp2, vp = vplayout(2, 1))
print(plot_58_sp3, vp = vplayout(2, 2))

dev.off()


