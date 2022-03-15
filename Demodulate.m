
% clc;
fPath = regexprep(mfilename('fullpath'),'\\demodulation_fft','');
fPath = 'C:\ADLINK\U-test\Recording';

% mDate = mDate(find(~cellfun(@isempty,strfind(model,'.dat'))));
filterOrder = 4;

model=dir(fPath);
mDate={model.date};
model={model.name};
model = model(~cellfun(@isempty,strfind(model,'.dat')));
mDate2 = datetime(mDate,'Format','yyyymmddhhmmss');

%ignore datetime format warning
[a, MSGID] = lastwarn();
warning('off', MSGID)

[c,d] = sort(mDate2);

datToUse = 'C:\ADLINK\U-test\Recording\Logging_data.dat';
nChannels = 3; nConnectedChannels = 3;



if (exist(regexprep(datToUse,'\.dat','\.mat'),'file') && isempty(strfind(datToUse, 'Logging_data')) && isempty(strfind(datToUse, 'ai_data')) )
    load(regexprep(datToUse,'\.dat','\.mat'));
else
fid = fopen(datToUse,'r');
temp = fread(fid, 'int16');
fclose(fid);
% temp = temp(end*(3.5/5):end*(4.5/5));



%Channels
if (nChannels==2)
    Chan1 = temp(1:2:floor(end/nChannels)*nChannels);
    Chan2 = temp(2:2:floor(end/nChannels)*nChannels);
elseif (nChannels==3)   
    Chan1 = temp(1:3:floor(end/nChannels)*nChannels);
    Chan2 = temp(2:3:floor(end/nChannels)*nChannels);
    Chan3 = temp(3:3:floor(end/nChannels)*nChannels);
elseif (nChannels==4)
    Chan1 = temp(1:4:floor(end/nChannels)*nChannels);
    Chan2 = temp(2:4:floor(end/nChannels)*nChannels);
    Chan3 = temp(3:4:floor(end/nChannels)*nChannels);
    Chan4 = temp(4:4:floor(end/nChannels)*nChannels);
end



%time axis
Fs = 1/2000000;
time =(1:length(Chan1));
time = Fs.*time;

% Get carrier freq
[A,B] = myRawFFT(time(1:1000),Chan1(1:1000));
[a,b]=max(A(:,2));
f0 = abs(A(b,1));


subTime = time(1:100)'-time(1);
shiftIndVal = findClosestPntInArr(1/f0/4, subTime);
Chan1WOffset = Chan1(shiftIndVal:end);
Chan1WOffset = Chan1WOffset(1:floor(length(Chan1WOffset)/4)*4);



Chan4 = Chan1;
nChannels = 4;


time = time(1:length(Chan1WOffset));
Chan1 = Chan1(1:length(Chan1WOffset));
Chan2 = Chan2(1:length(Chan1WOffset)) / 2913.1e-6; % The 2913.1 is a mapping from bin to uV
if (nChannels>=3)
    Chan3 = Chan3(1:length(Chan1WOffset)) / 2913.1e-6; % The 2913.1 is a mapping from bin to uV
end

if (nChannels>=4)
    Chan4 = Chan4(1:length(Chan1WOffset)) / 2913.1e-6; % The 2913.1 is a mapping from bin to uV
end

Chan1 = Chan1 + 1i*Chan1WOffset;
Chan1 = Chan1 / max(abs(Chan1(100:end-100))); % Normalize channel 1


figure(3)
if (nChannels>=3)
    figure(3);
    plot(1:101,real(Chan1(100:200)),  1:101,imag(Chan1(100:200)),  1:101,Chan2(100:200),  1:101,Chan3(100:200));
    
    figure(4);
    plot(1:101,Chan1((end-100:end)),  1:101,Chan2((end-100:end)),  1:101,Chan3(end-100:end));
end
if (nChannels>=4)
    figure(3);
    plot(1:101,real(Chan1(100:200)),  1:101,imag(Chan1(100:200)),  1:101,Chan2(100:200),  1:101,Chan3(100:200),  1:101,Chan4(100:200));
end

rawChan1 = Chan1;
rawChan2 = Chan2;


lowpass = f0 + 2.5E3;
highpass = f0 - 2.5E3;
[Chan1filtered] = filterData(time,Chan1, lowpass, highpass, filterOrder);
Chan1 = Chan1filtered;

MultipliedChannels = cell(2,1);
avg = {};
for chanInd = 1:(nChannels-1)
    
    
    
    lowpass = 107.1E3 + 2.5E3;
    highpass = 107.1E3 - 2.5E3;
    if (chanInd==1)
        MultipliedChannels{chanInd} = (Chan1.*Chan2);
        avg{chanInd} = mean(MultipliedChannels{chanInd});
        MultipliedChannels{chanInd} = MultipliedChannels{chanInd} - avg{chanInd};
    elseif(chanInd==2)
        MultipliedChannels{chanInd} = (Chan1.*Chan3);
        avg{chanInd} = mean(MultipliedChannels{chanInd});
        MultipliedChannels{chanInd} = MultipliedChannels{chanInd} - avg{chanInd};
    elseif(chanInd==3)
        MultipliedChannels{chanInd} = (Chan1.*Chan4);
        avg{chanInd} = mean(MultipliedChannels{chanInd});
        MultipliedChannels{chanInd} = MultipliedChannels{chanInd} - avg{chanInd};
    end
    
    
    lowpass = 1000;
    highpass = -1;
    [MultChanfiltered] = filterData(time,MultipliedChannels{chanInd}, lowpass, highpass, filterOrder);
    
    
    figure(chanInd)
    % yyaxis right
    MultChanfilteredLong{chanInd} = MultChanfiltered;
    MultChanfilteredShrt{chanInd} = MultChanfiltered(1:100:end);
    timeShrt = time(1:100:end);
    if (mod(length(MultChanfilteredShrt{chanInd}),2)==1)
        MultChanfilteredShrt{chanInd} = MultChanfilteredShrt{chanInd}(1:end-1);
        timeShrt = timeShrt(1:end-1);
    end
    plot(timeShrt,real(MultChanfilteredShrt{chanInd}),timeShrt,imag(MultChanfilteredShrt{chanInd}))
    ylabel('Volts (V)')
    hold off;
    figure(3)
    
    
    
end
if (isempty(strfind(datToUse, 'Logging_data')) && isempty(strfind(datToUse, 'ai_data')) )
save(regexprep(datToUse, '\.dat', '\.mat'),'MultChanfilteredShrt', 'timeShrt', 'avg');
end
end




figure(1)
MultChanfilteredShrt{2} = MultChanfilteredShrt{2}*1.0; % 250Hz-TripleCoil (3).dat



% SUBTRACT NOISE CHANNEL
y={};
for chanInd = 1:2
x = timeShrt(1:1000);
y1 = MultChanfilteredShrt{chanInd}(1:1000);
y2 = MultChanfilteredShrt{3}(1:1000);

k = trapz(x,y1.*y2)/trapz(x,y2.^2);

x = timeShrt;
y1 = MultChanfilteredShrt{chanInd};
y2 = MultChanfilteredShrt{3};

y{chanInd}=y1-k*y2;

figure(chanInd)
plot(x,abs(MultChanfilteredShrt{chanInd}),x,abs(y{chanInd})); 
plot(x,real(y{chanInd}), x,imag(y{chanInd})); 
 
plot(x,real(y{chanInd}), x,imag(y{chanInd})); 

end

figure(3)
plot(x,real(y{1}-y{2}), x,imag(y{1}-y{2})); 

MultChanfilteredShrt{1} = y{1};
MultChanfilteredShrt{2} = y{2};

MultChanfilteredShrtNrm = {};
MultChanfilteredShrtNrm{1} = abs(MultChanfilteredShrt{1}+avg{1});
MultChanfilteredShrtNrm{1} = MultChanfilteredShrtNrm{1} - mean(MultChanfilteredShrtNrm{1});
MultChanfilteredShrtNrm{2} = abs(MultChanfilteredShrt{2}+avg{2});
MultChanfilteredShrtNrm{2} = MultChanfilteredShrtNrm{2} - mean(MultChanfilteredShrtNrm{2});








