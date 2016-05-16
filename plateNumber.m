function plateNumber(name)
im = imread(name + '.bmp');
imbw = im2bw(im);
imthin = bwmorph(imbw, 'thin', Inf);
imshow(imthin);
saveas(gcf, name + 'thin.bmp');

