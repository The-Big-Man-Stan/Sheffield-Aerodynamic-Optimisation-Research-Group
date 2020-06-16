import time
import numpy as np
### </Summary>
### <Returns>
### A vector of CFD displacements as a numpy array.
### </Returns>
def IDWDeform(xyzVol, xyzSurf, dxyzVol, dxyzSurf):
	np.seterr(divide="raise")
	np.seterr(invalid="raise")
	# xyz = self.GetMeshUndeformedCoordinates()
	# dxyzSurf = self.GetDisplacements()
	# dxyzVol = np.zeros(xyz.shape)
	weights = np.ones(xyzSurf.shape[0])
	weights[25000] = 0
	
	for i in range(xyzVol.shape[0]):
		try:
			r = xyz[i] - xyzSurf
			#d = np.einsum('ij,ij->i', r, r)
			#weights = d*d # Equivalent of np.linalg(...) ** 4
			#weights = 1.0/weights
			weights = np.linalg.norm(r, axis=1) ** (-3.5)
		except:
			# Catch the div0 if the current volume point is
			# also a surface point.
			#surfInd = np.where(0.0 == weights)[0]
			#dxyzVol[i] = dxyzSurf[surfInd]
			continue
		
		weightSum = np.sum(weights)
		weights = weights/weightSum
		dxyzVol[i,0] = np.dot(weights, dxyzSurf[:,0])
		dxyzVol[i,1] = np.dot(weights, dxyzSurf[:,1])
		dxyzVol[i,2] = np.dot(weights, dxyzSurf[:,2])
	
	return dxyzVol

nvol = 6000000
nsurf = 50000

xyzVol = np.random.rand(nvol,3)
xyzSurf = np.random.rand(nsurf,3)
dxyzVol = np.zeros(xyzVol.shape)
dxyzSurf = np.random.rand(nsurf,3)

start = time.time()
dxyzVol = IDWDeform(xyzVol, xyzSurf, dxyzVol, dxyzSurf)
end = time.time()
seconds = end - start
print(f"Took {seconds} seconds")
print(f"Size {dxyzVol.shape}")