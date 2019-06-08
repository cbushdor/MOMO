SOURCE=studyRegardingProcessesAndPthread

all: texFile pdfFile

texFile: ${SOURCE}.tex 
	latex ${SOURCE}.tex

pdfFile: ${SOURCE}.dvi 
	dvipdf ${SOURCE}.dvi

clean:
	rm -f ${SOURCE}.{log,aux,pdf,dvi}
