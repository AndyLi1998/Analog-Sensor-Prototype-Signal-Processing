// This program demodulates data from the COTS MetalSCAN system

// Filtering is done using http://www.exstrom.com/journal/sigproc/

// DemodulateCOTSMSData.cpp : Defines the entry point for the console application.
//



#include <math.h>
#include <iostream>
#include <fstream>
#include "CompBasicFunctions.h"
#include "liir.h"
//#include <stdio.h>

#define edgeRemovalPnts 20000
#define maxPntCountPerDemod 10000000

int samplingRate = 2000000; // The sampling rate of the DAQ
int nOpenFiles = 0; // The number of files currently open

bool demodSignal(const char* fName, int nChannels, long long initlPnt, long long finlPnt); // Demodulates the given binary file and prints the result
double getDriveFreq(double** channelDatArr, double* time, int nPntsPerChannel, int nChannels, double* amplitude); // Returns the drive frequency calculated from channelDatArr
int findClosestPntInArr(double pointToFind, double* inArr, int arrSize); // Returns the index of the point in the given array
void filterData(double* time, complx* inArr, int arrSz, int filterOrder, double low, double high); // filters the data to pass the given range of frequencies

char curFName[1000];

char fnoutDat[1000];
char fnoutDat_Re[1000];
char fnoutDat_Im[1000];
char fntime[1000];

int main() {
	bool tmpBool;




	for (int k = 1; k <= 540; k++) {
		// Erase old output files
		FILE* file1; // Data file to demodulate

		snprintf(fnoutDat,sizeof(char)*1000, ".\\outDat_%d.txt", k);
		snprintf(fnoutDat_Re, sizeof(char) * 1000, ".\\outDat_Re_%d.bin", k);
		snprintf(fnoutDat_Im, sizeof(char) * 1000, ".\\outDat_Im_%d.bin", k);
		snprintf(fntime, sizeof(char) * 1000, ".\\time_%d.bin", k);

		fopen_s(&file1, fnoutDat, "w+"); if (file1) nOpenFiles++;
		fprintf(file1, "");
		fclose(file1); nOpenFiles--;
		fopen_s(&file1, fnoutDat_Re, "w+"); if (file1) nOpenFiles++;
		fprintf(file1, "");
		fclose(file1); nOpenFiles--;
		fopen_s(&file1, fnoutDat_Im, "w+"); if (file1) nOpenFiles++;
		fprintf(file1, "");
		fclose(file1); nOpenFiles--;
		fopen_s(&file1, fntime, "w+"); if (file1) nOpenFiles++;
		fprintf(file1, "");
		fclose(file1); nOpenFiles--;

		//// Get most recent file name
		//fopen_s(&file1, "C:\\ADLINK\\U-test\\Recording\\recentFName.txt", "r");
		//fscanf(file1, "%s", curFName);
		//fclose(file1);-----------add location
		char filename[1000];
		_snprintf_s(filename , sizeof(char) * 1000, sizeof(char) * 1000, "Multibore_3-4in_Bobbin_Crosstalk_Test_%d.dat", k);
		for (int i = 0; i < 100000; i++) {
			tmpBool = demodSignal(filename, 3, maxPntCountPerDemod * (unsigned long long)(i) - edgeRemovalPnts, maxPntCountPerDemod * ((unsigned long long)(i) + 1) + edgeRemovalPnts);
			//tmpBool = demodSignal("C:\\ADLINK\\U-test\\Recording\\Rev2BPlugFlow_Test014_d.dat", 3, maxPntCountPerDemod*(unsigned long long)(i) - edgeRemovalPnts, maxPntCountPerDemod*((unsigned long long)(i) + 1) + edgeRemovalPnts);
			if (tmpBool == 0) {
				break;
			}
		}
	}



	return 0;
}


// Demodulates the given binary file and prints the result
bool demodSignal(const char* fName, int nChannels, long long initlPnt, long long finlPnt) {
	// initlPnt : The index of the first point to demodulate
	// finlPnt : The index of the last point to demodulate
	FILE* file1; // Data file to demodulate
	unsigned long long fileSize; // Size of the data file
	double** channelDatArr; // Array of data for each of the channels
	complx** cmplxChannelDatArr; // Complex array of data for each of the channels
	int downSampleRate = 500; // The downsamples signal only takes 1 in every downSampleRate samples
	complx** demodDataArr; // Complex array of demodulated data
	int nDemodChannels; // The number of channels in the demodDataArr 
	unsigned long long nPntsPerDemodChannel; // The number of points in each channel of demodDataArr
	double* downSampledTime; // Time array for channelDatArr
	double* time; // Time array for channelDatArr
	unsigned long long nPntsPerChannel; // The number of points in each channel of channelDatArr
	double f0; // The drive frequency of the system
	double subTime[100]; // A subset of the time array used for calculating q offset
	int shiftIndVal; // The number of indices to shift the array in order to create a 90 degree ofset in the drive signal
	double chan0Amp; // The amplitude of channel 0 (i.e. the reference amplitude)
	int nChannels0 = nChannels; // The value of nChannels at the time of input 
	double* tmpArr;
	complx* tmpCmplxArr;
	complx avgComplxVal;
	__int16* tmpInt16Arr;
	unsigned long long nPntsInTmpInt16Arr;
	__int16 tmpInt16;
	double tmpVal;
	int i, j, k;
	int cntr;
	unsigned long long tmpInt;
	double lowFreqCutoff; // The low frequency cutoff used in filtering
	double highFreqCutoff; // The high frequency cutoff used in filterings

	// Read the binary file
	fopen_s(&file1, fName, "r"); if (file1) nOpenFiles++;

	// Get the file size
	fseek(file1, 0L, SEEK_END);
	fileSize = _ftelli64(file1);
	rewind(file1);
	nPntsInTmpInt16Arr = fileSize / sizeof(tmpInt16);//sizeof only care about data type
	nPntsPerChannel = (nPntsInTmpInt16Arr / (unsigned long long) nChannels);//unsign long long output need same input

	// Make sure the initlPnt and finlPnt make sense
	if (initlPnt < 0) initlPnt = 0;
	if (finlPnt >= nPntsPerChannel) finlPnt = nPntsPerChannel - 1;
	if (initlPnt > nPntsPerChannel) {
		return 0;
	}
	nPntsPerChannel = finlPnt - initlPnt + 1;
	if (nPntsPerChannel < 1) {
		return 0;
	}


	// Set up data arrays
	channelDatArr = new double* [nChannels];
	time = new double[nPntsPerChannel];
	//tmpInt16Arr = new __int16[nPntsInTmpInt16Arr];
	for (long long i = 0; i < nChannels; i++) {
		channelDatArr[i] = new double[nPntsPerChannel];
	}
	for (long long j = initlPnt; j <= finlPnt; j++) {
		time[j - initlPnt] = ((double)j) / samplingRate;
	}





	//tmpInt16Arr = new __int16[nPntsInTmpInt16Arr];
	//fread(tmpInt16Arr, nPntsInTmpInt16Arr, sizeof(tmpInt16), file1);
	//fclose(file1); nOpenFiles--;







	streampos size;
	char* memblock = new char[(finlPnt - initlPnt) * nChannels * sizeof(tmpInt16)];
	tmpInt16Arr = new __int16[(finlPnt - initlPnt) * nChannels];

	ifstream file(fName, ios::in | ios::binary | ios::ate);
	if (file.is_open())
	{
		size = file.tellg();
		file.seekg(initlPnt * nChannels * sizeof(tmpInt16), ios::beg);


		file.read(memblock, (finlPnt - initlPnt) * nChannels * sizeof(tmpInt16));
		file.close();

		cout << "Read " << (finlPnt * 100.) / (fileSize + 0.) * 6. << "%\n";

	}
	tmpInt16Arr = (__int16*)memblock;


	cntr = 0;
	for (long long glblInd = initlPnt * nChannels; glblInd < finlPnt * nChannels; glblInd++) {
		i = glblInd % nChannels;
		j = floor(glblInd / nChannels) - initlPnt;
		if (j < nPntsPerChannel) {
			channelDatArr[i][j] = (double)(tmpInt16Arr[cntr]);
		}
		cntr++;
	}

















	//// Read data into array
	//fread(tmpInt16Arr, nPntsInTmpInt16Arr, sizeof(tmpInt16), file1);
	//fclose(file1); nOpenFiles--;
	//for (int glblInd = initlPnt*nChannels; glblInd < finlPnt*nChannels; glblInd++) {
	//	i = glblInd % nChannels;
	//	j = floor(glblInd / nChannels) - initlPnt;
	//	if (j < nPntsPerChannel) {
	//		channelDatArr[i][j] = (double)tmpInt16Arr[glblInd];
	//	}
	//}







	//printf("TEST LINE\n"); {
	//	FILE *file1; // Data file to demodulate
	//	fopen_s(&file1, "outDat.txt", "w"); if (file1) nOpenFiles++;
	//	for (int i = 0; i < nPntsPerChannel; i++) {
	//		fprintf(file1, "%.15e\t%e%+ei\n", time[i], channelDatArr[0][i], 0.);
	//	}
	//	fclose(file1); nOpenFiles--;
	//}

	//for (int i = 100000; i < nPntsPerChannel; i+=100) {
	//	printf("%e ", time[i]);
	//	for (int j = 0; j < nChannels; j++) {
	//		printf("%e ", channelDatArr[i][j]);
	//	}
	//	printf("\n");
	//}

	// Get the drive frequency
	f0 = getDriveFreq(channelDatArr, time, nChannels, nPntsPerChannel, &chan0Amp);//-----------------whats it for?

	// Get offset for Channel 1             reference signal for imaginery part
	for (int i = 0; i < 100; i++) {
		subTime[i] = ((double)i) / samplingRate;
	}
	shiftIndVal = findClosestPntInArr(1 / f0 / 4., subTime, 100);//-----------------find value that points need to shift to achieve 90degree offset

	// Recreate the channel array in tmpArr
	cmplxChannelDatArr = new complx * [nChannels + 1];
	delete[] time;
	time = new double[nPntsPerChannel - shiftIndVal];
	for (int i = 0; i < nChannels + 1; i++) {
		cmplxChannelDatArr[i] = new complx[nPntsPerChannel - shiftIndVal];
		for (int j = 0; j < (nPntsPerChannel - shiftIndVal); j++) {
			time[j] = ((double)j + initlPnt) / samplingRate;
			if (i == 0) {//-------------?
				cmplxChannelDatArr[i][j] = newComplx(channelDatArr[i][j], channelDatArr[i][j + shiftIndVal]);
			}
			else if (i == nChannels) {
				cmplxChannelDatArr[i][j] = newComplx(channelDatArr[0][j], 0.) / 2913.1e-6; // The 2913.1 is a mapping from bin to uV
			}
			else {
				cmplxChannelDatArr[i][j] = newComplx(channelDatArr[i][j], 0.) / 2913.1e-6; // The 2913.1 is a mapping from bin to uV
			}
		}
	}
	////delete[] channelDatArr;
	nChannels++;//----------------copy of the refereence signl to reduce noise
	nPntsPerChannel = nPntsPerChannel - shiftIndVal;

	// Normalize the reference channel
	chan0Amp = 0.;
	for (int i = 1000; i < nPntsPerChannel - 1000; i++) {
		if (abs(cmplxChannelDatArr[0][i]) > chan0Amp) {
			chan0Amp = abs(cmplxChannelDatArr[0][i]);
		}
	}
	for (int i = 0; i < nPntsPerChannel; i++) {
		cmplxChannelDatArr[0][i] /= chan0Amp;
	}


	// Filter the data----------why this range?
	lowFreqCutoff = f0 + 2.5e3;
	highFreqCutoff = f0 - 2.5e3;
	//for (int chanInd = 0; chanInd < nChannels; chanInd++) {
	//	filterData(time, cmplxChannelDatArr[0], nPntsPerChannel, 4, lowFreqCutoff, highFreqCutoff);
	//}

	tmpCmplxArr = new complx[nPntsPerChannel];
	for (int chanInd = 1; chanInd < nChannels; chanInd++) {
		avgComplxVal = newComplx(0., 0.);
		tmpInt = 0;
		for (int i = 0; i < nPntsPerChannel; i++) {
			tmpCmplxArr[i] = cmplxChannelDatArr[0][i] * cmplxChannelDatArr[chanInd][i];
			//if (i > 200 && i < nPntsPerChannel - 200) {
			//	avgComplxVal += tmpCmplxArr[i];
			//	tmpInt++;
			//}
		}
		//avgComplxVal = avgComplxVal / tmpInt;
		//for (int i = 0; i < nPntsPerChannel; i++) {
		//	tmpCmplxArr[i] = tmpCmplxArr[i] - avgComplxVal;
		//}

		//printf("TEST LINE\n"); {
		//	FILE *file1; // Data file to demodulate
		//	fopen_s(&file1, "outDat.txt", "w"); if (file1) nOpenFiles++;
		//	for (int i = 0; i < nPntsPerChannel; i++) {
		//		fprintf(file1, "%.15e\t%e%+ei\n", time[i], tmpCmplxArr[i].real, tmpCmplxArr[i].imag);
		//	}
		//	fclose(file1); nOpenFiles--;
		//}

		lowFreqCutoff = -10;
		highFreqCutoff = 1000;
		filterData(time, tmpCmplxArr, nPntsPerChannel, 4, lowFreqCutoff, highFreqCutoff);
		for (int i = 0; i < nPntsPerChannel; i++) {
			cmplxChannelDatArr[chanInd][i] = tmpCmplxArr[i];
		}
	}


	// Make a downsampled demodulated array
	nDemodChannels = nChannels - 1;
	nPntsPerDemodChannel = 0;
	for (int j = edgeRemovalPnts; j < nPntsPerChannel - edgeRemovalPnts; j += downSampleRate) {
		nPntsPerDemodChannel++;
	}
	demodDataArr = new complx * [nDemodChannels];
	downSampledTime = new double[nPntsPerDemodChannel];
	for (int i = 1; i < nChannels; i++) {
		demodDataArr[i - 1] = new complx[nPntsPerDemodChannel];
		tmpInt = 0;
		for (int j = edgeRemovalPnts; j < nPntsPerChannel - edgeRemovalPnts; j += downSampleRate) {
			downSampledTime[tmpInt] = time[j];
			demodDataArr[i - 1][tmpInt] = cmplxChannelDatArr[i][j];
			tmpInt++;
		}
	}

	// Make real and imaginary demodDataArr arrays
	double* demodDataArr_Real = new double[nPntsPerDemodChannel * nDemodChannels];
	double* demodDataArr_Imag = new double[nPntsPerDemodChannel * nDemodChannels];
	cntr = 0;
	for (int i = 0; i < nPntsPerDemodChannel; i++) {
		for (int chanInd = 0; chanInd < nDemodChannels; chanInd++) {
			demodDataArr_Real[cntr] = demodDataArr[chanInd][i].real;
			demodDataArr_Imag[cntr] = demodDataArr[chanInd][i].imag;
			cntr++;
		}
	}


	// Print demodulated array
	fopen_s(&file1, fnoutDat, "a"); if (file1) nOpenFiles++;
	for (int i = 0; i < nPntsPerDemodChannel; i++) {
		fprintf(file1, "%.10e\t", downSampledTime[i]);
		for (int chanInd = 0; chanInd < nDemodChannels; chanInd++) {
			fprintf(file1, "%e%+ej\t", demodDataArr[chanInd][i].real, demodDataArr[chanInd][i].imag);
		}
		fprintf(file1, "\n");
	}
	fclose(file1); nOpenFiles--;

	fopen_s(&file1, fntime, "ab"); if (file1) nOpenFiles++;
	fwrite(downSampledTime, sizeof(double), nPntsPerDemodChannel, file1);
	fclose(file1); nOpenFiles--;

	fopen_s(&file1, fnoutDat_Re, "ab"); if (file1) nOpenFiles++;
	fwrite(demodDataArr_Real, sizeof(double), nPntsPerDemodChannel * nDemodChannels, file1);
	fclose(file1); nOpenFiles--;

	fopen_s(&file1, fnoutDat_Im, "ab"); if (file1) nOpenFiles++;
	fwrite(demodDataArr_Imag, sizeof(double), nPntsPerDemodChannel * nDemodChannels, file1);
	fclose(file1); nOpenFiles--;


	delete[] demodDataArr_Real;
	delete[] demodDataArr_Imag;
	delete[] time;
	delete[] tmpInt16Arr;
	for (int i = 0; i < nChannels0; i++) {
		delete[] channelDatArr[i];
		delete[] demodDataArr[i];
	}
	for (int i = 0; i < nChannels0 + 1; i++) {
		delete[] cmplxChannelDatArr[i];
	}
	delete[] channelDatArr;
	delete[] demodDataArr;
	delete[] cmplxChannelDatArr;
	delete[] downSampledTime;

	delete[]  tmpCmplxArr;
	//delete[] tmpInt16Arr;

	return 1;
}

// Returns the drive frequency calculated from channelDatArr
double getDriveFreq(double** channelDatArr, double* time, int nChannels, int nPntsPerChannel, double* amplitude) {
	double timeInit = 0;
	double timeFinl = 0;
	int nZeros;

	// Count the number of times that 0 is crossed
	nZeros = 0;
	*amplitude = 0.;
	for (int i = 1000; i < nPntsPerChannel - 1000; i++) {
		if (time[i] > 1.) {
			int a = 1;
		}

		if (absl(channelDatArr[0][i]) > * amplitude) {
			*amplitude = absl(channelDatArr[0][i]);
		}

		if (channelDatArr[0][i] * (double)channelDatArr[0][i - 1] < 0. || channelDatArr[0][i - 1] == 0.) {
			nZeros++;
			if (timeInit == 0.) {
				timeInit = time[i];
			}
			else {
				timeFinl = time[i];
			}
		}
	}

	return ((nZeros - 1) / 2. / (timeFinl - timeInit));
}


// Returns the index of the point in the given array
int findClosestPntInArr(double pointToFind, double* inArr, int arrSize) {
	double minDist; // The minimum distance between a point in inArr and pointToFind
	int minDistInd; // The index of the point in inArr with minimum distance to pointToFind

	minDist = 1e99;
	minDistInd = 0;
	for (int i = 0; i < arrSize; i++) {
		if (abs(inArr[i] - pointToFind) <= minDist) {
			minDist = abs(inArr[i] - pointToFind);
			minDistInd = i;
		}
	}
	return minDistInd;
}


// filters the data to pass the given range of frequencies
void filterData(double* time, complx* inArr, int arrSz, int filterOrder, double low, double high) {
	int nParams;// The number of c and d coefficients
	double* dParams; // "d" parameters for the butterworth filter
	int* cParams; // "c" parameters for the butterworth filter
	double sfParams; // The scaling factor for the butterworth filter
	complx* outArr; // The array to return (i.e. the filtered data)

	outArr = new complx[arrSz];

	low = low / samplingRate * 2;
	high = high / samplingRate * 2;

	if (low < 0.) {
		nParams = filterOrder + 1;
		dParams = dcof_bwlp(filterOrder, high);
		cParams = ccof_bwlp(filterOrder);
		sfParams = sf_bwlp(filterOrder, high);
	}
	else {
		nParams = 2 * filterOrder + 1;
		dParams = dcof_bwbp(filterOrder, low, high);
		cParams = ccof_bwbp(filterOrder);
		sfParams = sf_bwbp(filterOrder, low, high);
	}

	//printf("TEST LINE\n"); {
	//	for (int i = 0; i < nParams; i++) {
	//		printf("%e  ", dParams[i]);
	//		printf("%e  ", cParams[i] * sfParams);
	//		printf("%e\n", sfParams);
	//	}
	//}

	for (int i = 0; i < arrSz; i++) {
		outArr[i] = newComplx(0., 0.);
		if (i >= nParams) {
			for (int j = 0; j < nParams; j++) {
				outArr[i] += cParams[j] * sfParams * inArr[i - j];
			}
			for (int j = 1; j < nParams; j++) {
				outArr[i] += -1. * dParams[j] * outArr[i - j];
			}
		}
	}

	//printf("TEST LINE\n"); {
	//	FILE *file1; // Data file to demodulate
	//	fopen_s(&file1, "outDat.txt", "w"); if (file1) nOpenFiles++;
	//	for (int i = 0; i < arrSz; i++) {
	//		fprintf(file1, "%e\t%e%+ei\n", time[i], outArr[i].real, outArr[i].imag);
	//	}
	//	fclose(file1); nOpenFiles--;
	//}

	for (int i = 0; i < arrSz; i++) {
		inArr[i] = outArr[i];
	}
	delete[] outArr;
	return;
}


