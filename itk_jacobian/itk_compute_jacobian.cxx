// compute_jacobian.cpp
#include "itkImageFileReader.h"
#include "itkImageFileWriter.h"
#include "itkVector.h"
#include "itkVectorImage.h"
#include "itkDisplacementFieldTransform.h"
#include "itkImageRegionIteratorWithIndex.h"
#include "itkDisplacementFieldJacobianDeterminantFilter.h"
#include "vnl/vnl_det.h"

using PixelType = float;
constexpr unsigned int Dimension = 3;
using VectorPixelType = itk::Vector<PixelType, Dimension>;
using DisplacementFieldType = itk::Image<VectorPixelType, Dimension>;
using VectorImageType = itk::VectorImage<PixelType, Dimension>;
using ScalarImageType = itk::Image<PixelType, Dimension>;

int main(int argc, char *argv[])
{
  if (argc < 3)
  {
    std::cerr << "Usage: " << argv[0] << " displacement_field output_prefix" << std::endl;
    return EXIT_FAILURE;
  }

  const char *dispFilename = argv[1];
  const std::string outputPrefix = argv[2];

  using ReaderType = itk::ImageFileReader<DisplacementFieldType>;
  auto reader = ReaderType::New();
  reader->SetFileName(dispFilename);
  reader->Update();

  auto disp = reader->GetOutput();

  using TransformType = itk::DisplacementFieldTransform<PixelType, Dimension>;
  auto transform = TransformType::New();
  transform->SetDisplacementField(disp);

  auto region = disp->GetLargestPossibleRegion();
  auto size = region.GetSize();

  auto jacImage = VectorImageType::New();
  jacImage->SetRegions(region);
  jacImage->CopyInformation(disp);
  jacImage->SetNumberOfComponentsPerPixel(9);
  jacImage->Allocate();

  auto detImage = ScalarImageType::New();
  detImage->SetRegions(region);
  detImage->CopyInformation(disp);
  detImage->Allocate();

  using DispIterType = itk::ImageRegionIteratorWithIndex<DisplacementFieldType>;
  using JacIterType = itk::ImageRegionIterator<VectorImageType>;
  using DetIterType = itk::ImageRegionIterator<ScalarImageType>;

  JacIterType jacIt(jacImage, region);
  DetIterType detIt(detImage, region);

  for (DispIterType it(disp, region); !it.IsAtEnd(); ++it, ++jacIt, ++detIt)
  {
    itk::Index<Dimension> idx = it.GetIndex();
    TransformType::JacobianPositionType J;
    transform->ComputeJacobianWithRespectToPosition(idx, J);

    itk::VariableLengthVector<PixelType> flatJ(9);
    for (unsigned int i = 0; i < Dimension; ++i)
    {
      for (unsigned int j = 0; j < Dimension; ++j)
      {
        flatJ[i * Dimension + j] = static_cast<PixelType>(J[i][j]);
      }
    }
    jacIt.Set(flatJ);
    detIt.Set(static_cast<PixelType>(vnl_determinant(J)));
  }

  using WriterType1 = itk::ImageFileWriter<VectorImageType>;
  auto jacWriter = WriterType1::New();
  jacWriter->SetFileName(outputPrefix + "itk_transform_local_jacobian.nii.gz");
  jacWriter->SetInput(jacImage);
  jacWriter->Update();

  using WriterType2 = itk::ImageFileWriter<ScalarImageType>;
  auto detWriter = WriterType2::New();
  detWriter->SetFileName(outputPrefix + "itk_transform_local_jacobian_determinant.nii.gz");
  detWriter->SetInput(detImage);
  detWriter->Update();

  using DetFilterType = itk::DisplacementFieldJacobianDeterminantFilter<DisplacementFieldType, PixelType, ScalarImageType>;
  auto fdFilter = DetFilterType::New();
  fdFilter->SetInput(disp);
  fdFilter->SetUseImageSpacing(true);
  fdFilter->Update();

  auto fdWriter = WriterType2::New();
  fdWriter->SetFileName(outputPrefix + "itk_detfilter_jacobian_determinant.nii.gz");
  fdWriter->SetInput(fdFilter->GetOutput());
  fdWriter->Update();

  return EXIT_SUCCESS;
}

